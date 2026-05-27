"""Finance agent — the thin orchestrator that exists to prove the point.

Before this repo, a "finance agent" was a prompt plus a bag of inline
logic. Here it is six skill calls in a fixed sequence:

1. ``policy_lookup`` — get the policy snippet the action is grounded on.
2. ``permission_check`` — confirm the actor holds the permission.
3. ``document_search`` — pull supporting documents into the trace.
4. ``justification_draft`` — compose the justification text.
5. ``ticket_open`` — perform the side effect, if approved.
6. ``evidence_log`` — record what happened.

If a step refuses, the orchestrator stops there, records the refusal,
and returns it. Same path, every time. The same six skills back an HR
agent, an IT agent, or a customer-service agent. That is the whole point.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import ResultCategory, SkillResult, SkillTrace
from skill_first_ai.registry.registry import SkillRegistry


class FinanceRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    actor: str
    intent: str = Field(description="Free-text intent the user typed.")
    policy_topic: str
    required_permission: str
    ticket_title: str
    ticket_body: str


class FinanceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    decision: str
    ticket_id: str | None
    justification: str | None
    refusal_reason: str | None
    traces: tuple[SkillTrace, ...]


@dataclass(frozen=True)
class FinanceAgent:
    """An orchestrator that uses the registry — never imports skills directly.

    Importing skills directly inside the orchestrator would defeat the
    whole reusability story: it would couple the agent to specific
    implementations and bypass the registry's governance metadata.
    """

    registry: SkillRegistry

    def handle(self, request: FinanceRequest) -> FinanceResponse:
        traces: list[SkillTrace] = []

        # 1. policy_lookup
        policy = self._call("policy_lookup", {"topic": request.policy_topic}, traces)
        if policy.category is not ResultCategory.OK:
            return self._refuse(policy, request, traces, stage="policy_lookup")

        # 2. permission_check
        permission = self._call(
            "permission_check",
            {"actor": request.actor, "permission": request.required_permission},
            traces,
        )
        if permission.category is not ResultCategory.OK:
            return self._refuse(permission, request, traces, stage="permission_check")
        if permission.output is not None and not permission.output.allowed:  # type: ignore[attr-defined]
            return self._refuse(
                permission,
                request,
                traces,
                stage="permission_check",
                explicit_reason=permission.output.reason,  # type: ignore[attr-defined]
            )

        # 3. document_search (best-effort, non-blocking)
        self._call("document_search", {"query": request.intent[:90]}, traces)

        # 4. justification_draft
        justification = self._call(
            "justification_draft",
            {
                "actor": request.actor,
                "action": "ticket_open",
                "policy_topic": request.policy_topic,
                "rationale": request.intent,
            },
            traces,
        )

        # 5. ticket_open (the only side effect)
        ticket = self._call(
            "ticket_open",
            {
                "actor": request.actor,
                "category": "expense",
                "title": request.ticket_title,
                "body": request.ticket_body,
            },
            traces,
        )
        if ticket.category is not ResultCategory.OK or ticket.output is None:
            return self._refuse(ticket, request, traces, stage="ticket_open")
        ticket_id: str = ticket.output.ticket_id  # type: ignore[attr-defined]

        # 6. evidence_log
        self._call(
            "evidence_log",
            {
                "actor": request.actor,
                "action": "ticket_open",
                "decision": "executed",
                "correlation_id": ticket.trace.correlation_id,
                "notes": ticket_id,
            },
            traces,
        )

        return FinanceResponse(
            decision="executed",
            ticket_id=ticket_id,
            justification=(
                justification.output.text  # type: ignore[attr-defined]
                if justification.output is not None
                else None
            ),
            refusal_reason=None,
            traces=tuple(traces),
        )

    def _call(
        self,
        name: str,
        payload: dict[str, object],
        traces: list[SkillTrace],
    ) -> SkillResult[object]:
        result = self.registry.get(name).run(payload)
        traces.append(result.trace)
        return result

    @staticmethod
    def _refuse(
        result: SkillResult[object],
        request: FinanceRequest,
        traces: list[SkillTrace],
        *,
        stage: str,
        explicit_reason: str | None = None,
    ) -> FinanceResponse:
        return FinanceResponse(
            decision="refused",
            ticket_id=None,
            justification=None,
            refusal_reason=explicit_reason or f"{stage}: {result.message}",
            traces=tuple(traces),
        )
