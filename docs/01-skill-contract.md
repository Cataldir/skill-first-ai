# The skill contract

The contract has four jobs. Every skill in this repo satisfies all four.
Anything missing one is not a skill. It is a fragment of an agent that
slipped through review.

## Job 1 — Identity

```python
class SkillManifest(BaseModel):
    name: str            # stable, lower-snake-case
    version: str         # semver; breaking input/output = major bump
    description: str     # model-facing copy; every word read at runtime
    owner: str           # who maintains and approves changes
    tags: tuple[str, ...]
    side_effects: bool   # mutates state outside this process?
    pii: bool            # touches personal data?
    requires_approval: bool
```

- *Name* is how the registry finds it and how the MCP tool list publishes it.
- *Version* is how agents pin. Bump on any change to schemas. Patch versions
  are for behavior-equivalent fixes only.
- *Owner* is the human accountability anchor. The registry refuses skills
  without one — see `tests/test_governance.py::test_skill_has_complete_manifest`.

## Job 2 — Translation

```python
class InputSchema(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    ...

class OutputSchema(BaseModel):
    model_config = ConfigDict(frozen=True)
    ...
```

- The input schema uses `extra="forbid"` — unexpected fields fail loudly
  instead of silently dropping. This is the cheapest defense against
  prompt-injected payload smuggling.
- The output schema is the same shape every consumer reads. Foundry agent,
  MCP client, FastAPI consumer, internal Python caller — all get the same
  Pydantic model.

## Job 3 — Failure categorization

```python
class ResultCategory(str, Enum):
    OK = "ok"
    INVALID_INPUT = "invalid_input"
    REFUSED = "refused"
    TEMPORARY_FAILURE = "temporary_failure"
```

- `OK` — the skill did its job; the output is in `result.output`.
- `INVALID_INPUT` — the payload failed validation. Do not retry without
  changing the input.
- `REFUSED` — policy refused the action. **Not a failure.** Surface to the
  user; do not retry.
- `TEMPORARY_FAILURE` — a downstream system was momentarily unavailable.
  Retry with the same correlation id.

The agent never has to invent retry logic. The category tells it what to do.

## Job 4 — Evidence

```python
class SkillTrace(BaseModel):
    correlation_id: str
    skill_name: str
    skill_version: str
    latency_ms: float
    category: ResultCategory
```

- Frozen dataclass-style model: traces cannot be mutated after creation.
- Correlation IDs chain across the orchestrator so a single user turn can
  be reconstructed end-to-end.
- The auditor's question — *"why did the agent open this ticket?"* — is
  answered by playing back the trace, not by asking the model what it
  thought yesterday.

## The envelope

```python
class SkillResult(BaseModel, Generic[OutputT]):
    category: ResultCategory
    output: OutputT | None
    message: str
    trace: SkillTrace
```

The same envelope every consumer reads. If you find yourself returning a
custom envelope for a specific consumer, you are inventing a private
contract — and the registry's value evaporates the moment you do.

## What changes the contract

Only these changes require a version bump:

| Change | Bump |
|--------|------|
| New required input field | major |
| Removed input field | major |
| Changed type or constraint of an input field | major |
| New required output field | major |
| Removed output field | major |
| Changed type or constraint of an output field | major |
| New optional input field | minor |
| New optional output field | minor |
| Behavior change with identical schemas | minor (document it) |
| Bug fix with identical schemas | patch |

Goldens in `tests/_golden_schemas/` enforce the schema half of this rule.

## Anti-patterns to flag in review

- Skill returns a dict instead of a Pydantic model.
- Skill raises `Exception` instead of a typed `SkillError` subclass.
- Skill returns `OK` with `output=None` to mean "soft failure". (Use a category.)
- Skill silently retries a transient downstream. (Surface `TEMPORARY_FAILURE`.)
- Skill mutates a global without recording it in evidence.
- Two skills with the same name and different shapes. (Pick one; deprecate the other.)
