"""``document_search`` — find documents related to a free-text query.

The skill returns titles, URIs, and a short snippet. It does *not*
return the body. The orchestrator decides whether to follow up with a
read. That separation keeps the search surface narrow enough to govern.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import BaseSkill, SkillManifest

_DEMO_INDEX: tuple[dict[str, str], ...] = (
    {
        "title": "FY26 Travel Policy",
        "uri": "https://intranet.contoso.com/policies/travel-fy26",
        "snippet": (
            "Domestic flights default to economy. Hotels reimbursed up to "
            "USD 250 per night. Director approval required above USD 1500."
        ),
        "tags": "travel expense policy",
    },
    {
        "title": "Vacation Request Form",
        "uri": "https://intranet.contoso.com/forms/vacation",
        "snippet": (
            "Standard vacation request form. Up to 15 days requires manager "
            "approval; above 15 days requires second-level approval."
        ),
        "tags": "vacation hr leave",
    },
    {
        "title": "Production Access Standard",
        "uri": "https://intranet.contoso.com/security/prod-access",
        "snippet": (
            "Production access requires CAB ticket and two-person approval. "
            "Maximum 8 hours per request, time-bound."
        ),
        "tags": "access security production",
    },
    {
        "title": "Refund Decision Tree",
        "uri": "https://intranet.contoso.com/cs/refund-tree",
        "snippet": (
            "Decision tree for customer refund eligibility. Up to USD 100 is "
            "auto-approved; above requires supervisor review."
        ),
        "tags": "refund customer service",
    },
)


class DocumentSearchInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    query: str = Field(description="Free-text query, 3-100 chars.", min_length=3, max_length=100)
    limit: int = Field(default=3, ge=1, le=5)


class DocumentHit(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str
    uri: str
    snippet: str


class DocumentSearchOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    query: str
    hits: tuple[DocumentHit, ...]


class DocumentSearch(BaseSkill[DocumentSearchInput, DocumentSearchOutput]):
    InputSchema: ClassVar[type[BaseModel]] = DocumentSearchInput
    OutputSchema: ClassVar[type[BaseModel]] = DocumentSearchOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="document_search",
        version="1.0.0",
        description=(
            "Search the intranet document index. Returns titles, URIs and "
            "snippets only. Use when the user asks where to find something."
        ),
        owner="Knowledge Operations",
        tags=("search", "knowledge"),
        side_effects=False,
        pii=False,
    )

    def _execute(self, payload: DocumentSearchInput) -> DocumentSearchOutput:
        terms = {token for token in payload.query.lower().split() if len(token) > 2}
        scored: list[tuple[int, dict[str, str]]] = []
        for doc in _DEMO_INDEX:
            haystack = f"{doc['title']} {doc['snippet']} {doc['tags']}".lower()
            score = sum(1 for term in terms if term in haystack)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        top = scored[: payload.limit]
        return DocumentSearchOutput(
            query=payload.query,
            hits=tuple(
                DocumentHit(title=doc["title"], uri=doc["uri"], snippet=doc["snippet"])
                for _, doc in top
            ),
        )
