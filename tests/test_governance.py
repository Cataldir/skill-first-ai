"""Governance tests — the contract every registered skill must satisfy.

These tests are what makes the registry safe to publish across teams.
If they pass, a new skill *cannot* land without an owner, a description,
side-effect annotation, and PII classification.

This is also the slide that wins half the talk. Run them live in the
demo: ``pytest tests/test_governance.py -v``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import BaseModel

from skill_first_ai.contracts.skill import BaseSkill, SkillManifest
from skill_first_ai.registry.registry import default_registry

GOLDEN_DIR = Path(__file__).parent / "_golden_schemas"


@pytest.fixture(scope="module")
def registry():
    return default_registry()


def test_registry_is_not_empty(registry):
    assert len(registry) >= 6, "the demo expects the six provocation skills"


@pytest.mark.parametrize(
    "skill",
    list(default_registry()),
    ids=lambda s: s.manifest.name,
)
def test_skill_has_complete_manifest(skill: BaseSkill):
    manifest: SkillManifest = skill.manifest
    assert manifest.name and manifest.name == manifest.name.lower()
    assert manifest.version and manifest.version.count(".") == 2
    assert manifest.description and len(manifest.description) >= 40
    assert manifest.owner, f"{manifest.name} has no owner; refusing to register"


@pytest.mark.parametrize(
    "skill",
    list(default_registry()),
    ids=lambda s: s.manifest.name,
)
def test_skill_declares_schemas(skill: BaseSkill):
    assert issubclass(skill.InputSchema, BaseModel)
    assert issubclass(skill.OutputSchema, BaseModel)
    # Forbid silent input expansion: every schema must use ``extra='forbid'``
    # or declare it OK on purpose. We assert ``forbid`` for input only.
    config = getattr(skill.InputSchema, "model_config", {})
    assert config.get("extra") == "forbid", (
        f"{skill.manifest.name}: InputSchema must set extra='forbid' "
        "so unexpected fields are caught instead of ignored."
    )


@pytest.mark.parametrize(
    "skill",
    list(default_registry()),
    ids=lambda s: s.manifest.name,
)
def test_side_effecting_skills_require_pii_review(skill: BaseSkill):
    if skill.manifest.side_effects:
        assert skill.manifest.pii is True, (
            f"{skill.manifest.name}: side-effecting skills must declare "
            "pii=True so they route through the PII review pipeline."
        )


@pytest.mark.parametrize(
    "skill",
    list(default_registry()),
    ids=lambda s: s.manifest.name,
)
def test_skill_input_schema_matches_golden(skill: BaseSkill):
    """Golden JSON-schema snapshot test.

    The first time a skill ships, the test writes the golden file and
    passes. Subsequent runs diff against the golden. Changing the input
    shape now requires a version bump and a deliberate refresh, which is
    exactly the governance the talk argues for.

    Refresh deliberately with ``pytest --update-golden`` (see conftest).
    """
    GOLDEN_DIR.mkdir(exist_ok=True)
    golden = GOLDEN_DIR / f"{skill.manifest.name}.input.json"
    schema = skill.InputSchema.model_json_schema()
    if not golden.exists():
        golden.write_text(json.dumps(schema, indent=2, sort_keys=True))
        pytest.skip(f"wrote new golden for {skill.manifest.name}")
    expected = json.loads(golden.read_text())
    assert schema == expected, (
        f"{skill.manifest.name}: input schema drifted from golden. "
        "Bump the version and refresh the golden deliberately."
    )
