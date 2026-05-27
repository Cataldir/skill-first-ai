# Governance — test, version, govern

Governance is what turns "interesting demo" into "thing several teams can
rely on." It runs at three timescales: per commit (tests), per release
(versioning), per quarter (review).

## Per commit — tests

Three test suites. All run on every commit. None of them is optional.

### Unit tests (`tests/test_skills_unit.py`)

One test per documented behavior:

- Happy path with valid input → `category == OK`.
- Validation failure → `category == INVALID_INPUT`.
- Policy refusal → `category == REFUSED`.
- Transient downstream → `category == TEMPORARY_FAILURE`.

These tests are cheap. Write them first.

### Governance tests (`tests/test_governance.py`)

The contract-level tests. The ones that should run live in the demo.

- `test_skill_has_complete_manifest` — name, version, description,
  owner present. Description must be at least 40 characters.
- `test_skill_declares_schemas` — both Input and Output are Pydantic
  models. Input has `extra="forbid"`.
- `test_side_effecting_skills_require_pii_review` — if
  `manifest.side_effects` is True, `manifest.pii` must be True.
- `test_skill_input_schema_matches_golden` — diff input JSON schema
  against a stored golden in `tests/_golden_schemas/`. Drift fails the test.

These tests are why a skill survives a year of refactors without silently
breaking the agents that depend on it.

### Orchestrator tests (`tests/test_orchestrator.py`)

The decision-flow tests:

- Happy path executes and writes evidence.
- Permission denial refuses and writes no evidence-of-execution.
- Unknown actor refuses early; no downstream calls happen.

Run these on every commit. They are the cheapest way to detect that someone
wired a new skill into the orchestrator and skipped a check.

## Per release — versioning

Three rules:

1. **Semver on the manifest.** Major bumps mean breaking schema or behavior
   change. Minor bumps mean new optional fields or strictly additive behavior.
   Patch bumps mean bug fixes that preserve schemas.

2. **Agents pin major.** A Foundry agent definition references
   `policy_lookup` (latest major) — never an exact patch. Upgrades happen
   when the team is ready, not when CI says so.

3. **Goldens are the source of truth for schemas.** Refresh deliberately:

   ```powershell
   # Inspect, then either accept (and commit) or fix the schema.
   pytest tests/test_governance.py::test_skill_input_schema_matches_golden -v
   ```

   The first run after a new skill writes the golden and reports a skip.
   Subsequent runs diff.

## Per quarter — review

Two artifacts get reviewed by a human:

### The catalog

A markdown report generated from the registry:

```python
from skill_first_ai.registry import default_registry
for manifest in default_registry().manifests():
    print(f"- **{manifest.name}** v{manifest.version} — {manifest.owner}")
```

The reviewer asks:

- Are owners still active in the team?
- Are descriptions still accurate?
- Are there skills that have been deprecated by combinations of others?
- Are there duplicates with different names?

### The evidence sample

A sample of `evidence_log` rows from the last quarter. The reviewer asks:

- Were refusals surfaced to the user, or silently dropped?
- Were any decisions made by the agent that should have been workflows?
- Were any skills called without the corresponding `permission_check`?

If the answers are uncomfortable, the registry needs a new test, not a
new agent.

## What governance does *not* do

- It does not gate every commit on a human. The tests are the gate.
- It does not require a Center of Excellence. The owner field is per skill.
- It does not block the team from shipping. Goldens are refreshed
  deliberately, not feared.

## What governance *does* do

- It prevents the skill registry from accidentally turning into a junk
  drawer of half-finished agent fragments.
- It makes the conversation in committee a different conversation:
  *"which skill is this missing?"* instead of *"should we build another agent?"*
- It gives the audit team something to inspect that is not a transcript.
