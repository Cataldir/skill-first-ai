"""``justification_draft`` — return a short, structured justification
text for an action.

The skill itself is the cheapest one in the catalog because it does *not*
call a language model. It composes a deterministic, auditable string from
the policy, the actor, the action, and any free-form rationale the agent
already had.

If a team later swaps this for an LLM-backed implementation, the
contract does not change. The output is still ``JustificationOutput``
with the same fields. The agent code does not move.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import BaseSkill, SkillManifest


class JustificationInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    actor: str = Field(description="The actor whose action is being justified.")
    action: str = Field(description="The action being justified, e.g. ticket_open.")
    policy_topic: str = Field(description="Policy topic the action is grounded on.")
    rationale: str = Field(
        description="Free-form rationale the orchestrator inferred from context.",
        max_length=600,
    )


class JustificationOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    text: str
    citations: tuple[str, ...]


class JustificationDraft(BaseSkill[JustificationInput, JustificationOutput]):
    InputSchema: ClassVar[type[BaseModel]] = JustificationInput
    OutputSchema: ClassVar[type[BaseModel]] = JustificationOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="justification_draft",
        version="1.0.0",
        description=(
            "Compose a short, structured justification for an action. "
            "Deterministic by default — swap for an LLM-backed version "
            "behind the same contract."
        ),
        owner="Compliance Engineering",
        tags=("text", "audit"),
        side_effects=False,
        pii=True,
    )

    def _execute(self, payload: JustificationInput) -> JustificationOutput:
        text = (
            f"Action {payload.action} requested by {payload.actor}. "
            f"Grounded on policy {payload.policy_topic}. "
            f"Rationale: {payload.rationale.strip()}"
        )
        citations = (f"policy:{payload.policy_topic}",)
        return JustificationOutput(text=text, citations=citations)
