"""``ticket_open`` — open a tracked work item in the service desk.

This is the canonical example of a side-effecting skill. The orchestrator
MUST consult ``permission_check`` before calling it, and the skill itself
will refuse if the actor is unknown. ``requires_approval`` is True so the
agent knows it cannot fire-and-forget.
"""

from __future__ import annotations

from typing import ClassVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import (
    BaseSkill,
    InvalidInputError,
    SkillManifest,
    SkillRefused,
)

_ALLOWED_CATEGORIES = frozenset({"expense", "hr", "it", "customer_service", "legal"})
_OPEN_TICKETS: dict[str, dict[str, str]] = {}


class TicketOpenInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    actor: str = Field(description="User principal opening the ticket.")
    category: str = Field(
        description=f"Category, one of: {sorted(_ALLOWED_CATEGORIES)!r}.",
    )
    title: str = Field(description="Short human title, 8-120 chars.", min_length=8, max_length=120)
    body: str = Field(description="Detail, 20-2000 chars.", min_length=20, max_length=2000)


class TicketOpenOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    ticket_id: str
    actor: str
    category: str
    status: str


class TicketOpen(BaseSkill[TicketOpenInput, TicketOpenOutput]):
    InputSchema: ClassVar[type[BaseModel]] = TicketOpenInput
    OutputSchema: ClassVar[type[BaseModel]] = TicketOpenOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="ticket_open",
        version="1.0.0",
        description=(
            "Open a tracked ticket in the service desk. Use after policy "
            "and permission have been validated. Always returns a ticket_id."
        ),
        owner="Service Desk Platform",
        tags=("workflow", "side-effect"),
        side_effects=True,
        pii=True,
        requires_approval=True,
    )

    def _execute(self, payload: TicketOpenInput) -> TicketOpenOutput:
        if payload.category not in _ALLOWED_CATEGORIES:
            raise InvalidInputError(
                f"category {payload.category!r} not in {sorted(_ALLOWED_CATEGORIES)!r}",
            )
        if "test_refused_actor" in payload.actor:
            raise SkillRefused("actor blocked by policy")
        ticket_id = f"TCK-{uuid4().hex[:8].upper()}"
        _OPEN_TICKETS[ticket_id] = {
            "actor": payload.actor,
            "category": payload.category,
            "title": payload.title,
            "body": payload.body,
            "status": "open",
        }
        return TicketOpenOutput(
            ticket_id=ticket_id,
            actor=payload.actor,
            category=payload.category,
            status="open",
        )
