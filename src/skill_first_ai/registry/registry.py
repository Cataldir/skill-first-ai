"""Skill registry — the single place skills get listed, versioned, and
exposed.

The registry is intentionally boring. It holds skill instances by name,
returns manifests for governance review, and refuses to register two
skills with the same name and version. Anything fancier (semantic search
over manifests, multi-tenant scoping, A/B routing) is a separate concern
that belongs in a different layer.

The same registry feeds every consumer:

- The Foundry **prompt agent** (via the MCP server in ``foundry.mcp_server``).
- The Foundry **Hosted agent** option (a thin Python orchestrator).
- A local FastAPI wrapper if the team wants HTTP.
- Direct Python imports inside the codebase.

That is the point. One registry, many consumers. Anyone trying to fork
the registry into "the HR registry" and "the finance registry" is
recreating the agent sprawl problem one level down.
"""

from __future__ import annotations

from collections.abc import Iterator

from skill_first_ai.contracts.skill import BaseSkill, SkillManifest


class DuplicateSkillError(ValueError):
    """Raised when a skill is registered twice under the same name+version."""


class UnknownSkillError(KeyError):
    """Raised when a caller asks for a skill that is not registered."""


class SkillRegistry:
    """In-memory registry of skill instances keyed by manifest name."""

    def __init__(self) -> None:
        self._skills: dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill) -> None:
        key = self._key(skill.manifest.name, skill.manifest.version)
        if key in self._skills:
            raise DuplicateSkillError(
                f"Skill {key!r} already registered. Bump the version or rename.",
            )
        self._skills[key] = skill

    def get(self, name: str, version: str | None = None) -> BaseSkill:
        if version is not None:
            try:
                return self._skills[self._key(name, version)]
            except KeyError as exc:
                raise UnknownSkillError(name) from exc

        matches = [
            (key, skill)
            for key, skill in self._skills.items()
            if skill.manifest.name == name
        ]
        if not matches:
            raise UnknownSkillError(name)
        matches.sort(key=lambda item: item[1].manifest.version, reverse=True)
        return matches[0][1]

    def manifests(self) -> tuple[SkillManifest, ...]:
        return tuple(skill.manifest for skill in self._skills.values())

    def __iter__(self) -> Iterator[BaseSkill]:
        return iter(self._skills.values())

    def __len__(self) -> int:
        return len(self._skills)

    @staticmethod
    def _key(name: str, version: str) -> str:
        return f"{name}@{version}"


def default_registry() -> SkillRegistry:
    """Build the registry every consumer in this repo starts from.

    Add new skills here in one place. If a skill is not in this list, no
    agent should be able to call it. That is the whole governance story
    in five lines of code.
    """
    from skill_first_ai.skills.document_search import DocumentSearch
    from skill_first_ai.skills.evidence_log import EvidenceLog
    from skill_first_ai.skills.justification import JustificationDraft
    from skill_first_ai.skills.permission_check import PermissionCheck
    from skill_first_ai.skills.policy_lookup import PolicyLookup
    from skill_first_ai.skills.ticket_open import TicketOpen

    registry = SkillRegistry()
    registry.register(PolicyLookup())
    registry.register(PermissionCheck())
    registry.register(DocumentSearch())
    registry.register(TicketOpen())
    registry.register(EvidenceLog())
    registry.register(JustificationDraft())
    return registry
