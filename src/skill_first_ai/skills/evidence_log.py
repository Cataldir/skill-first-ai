"""``evidence_log`` — append an evidence entry for an action the
orchestrator took.

This is the cheapest skill in the catalog and the one most teams skip,
which is also why their agent systems are impossible to audit later.
The skill writes one row per side-effecting decision, with correlation
ID and a tag the auditor can filter by.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import BaseSkill, SkillManifest

_EVIDENCE_LOG: list[dict[str, str]] = []


class EvidenceLogInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    actor: str = Field(description="Who performed the action.")
    action: str = Field(description="What was attempted, e.g. ticket_open, refund_approve.")
    decision: str = Field(description="executed | refused | escalated.")
    correlation_id: str = Field(description="The trace ID linking the action chain.")
    notes: str = Field(default="", max_length=2000)


class EvidenceLogOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    evidence_id: str
    recorded_at: str


class EvidenceLog(BaseSkill[EvidenceLogInput, EvidenceLogOutput]):
    InputSchema: ClassVar[type[BaseModel]] = EvidenceLogInput
    OutputSchema: ClassVar[type[BaseModel]] = EvidenceLogOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="evidence_log",
        version="1.0.0",
        description=(
            "Append an evidence row for an action the agent took. Use after "
            "every side-effecting skill so the audit trail exists tomorrow."
        ),
        owner="Compliance Engineering",
        tags=("governance", "audit"),
        side_effects=True,
        pii=True,
    )

    def _execute(self, payload: EvidenceLogInput) -> EvidenceLogOutput:
        evidence_id = f"EVD-{uuid4().hex[:10].upper()}"
        recorded_at = datetime.now(tz=timezone.utc).isoformat()
        _EVIDENCE_LOG.append(
            {
                "evidence_id": evidence_id,
                "recorded_at": recorded_at,
                "actor": payload.actor,
                "action": payload.action,
                "decision": payload.decision,
                "correlation_id": payload.correlation_id,
                "notes": payload.notes,
            },
        )
        return EvidenceLogOutput(evidence_id=evidence_id, recorded_at=recorded_at)


def evidence_dump() -> tuple[dict[str, str], ...]:
    """Read-only access to the demo evidence buffer, used by tests and
    by the demo CLI."""
    return tuple(_EVIDENCE_LOG)


def evidence_reset() -> None:
    """Clear the demo evidence buffer between tests. Not exposed via
    the registry or MCP server."""
    _EVIDENCE_LOG.clear()
