"""``permission_check`` — does this actor have this permission?

Reused by every domain. The mistake people make is letting each domain
agent re-implement permission logic in prompt form. The cost is that
the answer is inconsistent and the audit trail is in a model's head.
This skill is the only place that decides.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from skill_first_ai.contracts.skill import (
    BaseSkill,
    SkillManifest,
    SkillRefused,
)

# Demo permission table. Production swaps for Entra ID groups, RBAC, or
# a dedicated policy engine. The contract is identical.
_DEMO_ROLES: dict[str, frozenset[str]] = {
    "alice@contoso.com": frozenset(
        {"expense.read", "expense.submit", "hr.vacation.request"},
    ),
    "bob@contoso.com": frozenset(
        {
            "expense.read",
            "expense.approve",
            "hr.vacation.request",
            "it.access.request",
        },
    ),
    "carol@contoso.com": frozenset(
        {
            "expense.read",
            "expense.approve",
            "expense.policy.edit",
            "hr.vacation.approve",
        },
    ),
}


class PermissionCheckInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    actor: str = Field(description="User principal name, e.g. alice@contoso.com.")
    permission: str = Field(
        description=(
            "Dotted permission identifier, e.g. expense.submit, "
            "expense.approve, hr.vacation.approve, it.access.request."
        ),
    )


class PermissionCheckOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    actor: str
    permission: str
    allowed: bool
    reason: str


class PermissionCheck(BaseSkill[PermissionCheckInput, PermissionCheckOutput]):
    InputSchema: ClassVar[type[BaseModel]] = PermissionCheckInput
    OutputSchema: ClassVar[type[BaseModel]] = PermissionCheckOutput
    manifest: ClassVar[SkillManifest] = SkillManifest(
        name="permission_check",
        version="1.0.0",
        description=(
            "Return whether an actor holds a permission. Use before any "
            "side-effecting skill (ticket_open, evidence_log writes, "
            "spend approvals)."
        ),
        owner="Platform Security",
        tags=("authorization", "governance"),
        side_effects=False,
        pii=True,
    )

    def _execute(self, payload: PermissionCheckInput) -> PermissionCheckOutput:
        granted = _DEMO_ROLES.get(payload.actor, frozenset())
        if payload.actor not in _DEMO_ROLES:
            # Unknown actors are refused, not 500'd. The agent then
            # surfaces the message to the user instead of pretending the
            # request went through.
            raise SkillRefused(
                f"unknown actor: {payload.actor!r}; refuse by default",
            )
        allowed = payload.permission in granted
        reason = (
            "permission granted by directory role"
            if allowed
            else "actor does not hold the requested permission"
        )
        return PermissionCheckOutput(
            actor=payload.actor,
            permission=payload.permission,
            allowed=allowed,
            reason=reason,
        )
