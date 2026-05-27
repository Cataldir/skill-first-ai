"""Skill-first AI: fewer agents, more reusable capabilities.

Public exports for the most common imports. Everything else lives
under explicit submodules so the boundaries stay visible.
"""

from skill_first_ai.contracts.skill import (
    BaseSkill,
    ResultCategory,
    SkillManifest,
    SkillResult,
    SkillTrace,
)
from skill_first_ai.registry.registry import SkillRegistry

__all__ = [
    "BaseSkill",
    "ResultCategory",
    "SkillManifest",
    "SkillRegistry",
    "SkillResult",
    "SkillTrace",
]
