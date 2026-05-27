"""``policy_lookup`` — find the canonical policy snippet for a topic.

Reused by finance (expense policy), HR (travel policy, vacation),
IT (access policy), and customer service (refund policy). Without this
skill, every domain agent would carry its own retrieval logic. With it,
the policy source of truth is one place to fix.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import (
    BaseSkill,
    InvalidInputError,
    SkillManifest,
)

# Stand-in for whatever the real policy store is. A demo registry is
# enough to make the contract honest; production swaps the dict for
# Azure AI Search, Cosmos DB, SharePoint, or a vector index.
_DEMO_POLICIES: dict[str, dict[str, str]] = {
    "expense.travel": {
        "summary": (
            "Travel above USD 1500 requires director approval. Domestic "
            "flights default to economy. Hotels reimbursed up to USD 250/night."
        ),
        "owner": "Finance Operations",
        "last_reviewed": "2026-02-14",
    },
    "expense.meals": {
        "summary": (
            "Meals up to USD 80 per person per day. Receipts required above "
            "USD 25. Alcohol is not reimbursed."
        ),
        "owner": "Finance Operations",
        "last_reviewed": "2025-11-03",
    },
    "hr.vacation": {
        "summary": (
            "30 calendar days per year, split into up to three periods. "
            "Requests below 15 days need manager approval; above 15 days "
            "need second-level approval."
        ),
        "owner": "People Operations",
        "last_reviewed": "2026-01-20",
    },
    "it.access.production": {
        "summary": (
            "Production access requires CAB ticket plus two-person approval. "
            "Time-bound: maximum 8 hours per request."
        ),
        "owner": "Platform Security",
        "last_reviewed": "2026-04-09",
    },
}


class PolicyLookupInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    topic: str = Field(
        description=(
            "Policy topic in dotted form, e.g. expense.travel, hr.vacation, "
            "it.access.production."
        ),
    )


class PolicyLookupOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    topic: str
    summary: str
    owner: str
    last_reviewed: str


class PolicyLookup(BaseSkill[PolicyLookupInput, PolicyLookupOutput]):
    InputSchema: ClassVar[type[BaseModel]] = PolicyLookupInput
    OutputSchema: ClassVar[type[BaseModel]] = PolicyLookupOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="policy_lookup",
        version="1.0.0",
        description=(
            "Return the canonical policy snippet for a topic. Use when the "
            "user asks what a policy says or whether something is allowed."
        ),
        owner="Finance Operations + People Operations",
        tags=("policy", "knowledge"),
        side_effects=False,
        pii=False,
    )

    def _execute(self, payload: PolicyLookupInput) -> PolicyLookupOutput:
        record = _DEMO_POLICIES.get(payload.topic)
        if record is None:
            raise InvalidInputError(
                f"unknown policy topic: {payload.topic!r}. "
                f"Known: {sorted(_DEMO_POLICIES)!r}",
            )
        return PolicyLookupOutput(
            topic=payload.topic,
            summary=record["summary"],
            owner=record["owner"],
            last_reviewed=record["last_reviewed"],
        )
