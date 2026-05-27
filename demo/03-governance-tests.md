# Demo 3 · Governance pytest

**Slide cue**: slide 11.
**Target duration**: ~2 minutes.
**Goal**: show that governance is enforced by CI, not by ceremony.

## Steps

1. Terminal large. Repo root. Run:
   ```powershell
   uv run pytest tests/test_governance.py -v
   ```
2. Read the test names aloud as they pass:
   - `test_registry_is_not_empty`
   - `test_skill_has_complete_manifest[policy_lookup]`
   - `test_skill_has_complete_manifest[permission_check]`
   - `test_skill_has_complete_manifest[...]`
   - `test_skill_declares_schemas[...]`
   - `test_side_effecting_skills_require_pii_review[...]`
   - `test_skill_input_schema_matches_golden[...]`
3. Say:
   > *"esses testes não testam a skill. Testam o contrato. Sem owner, sem
   > schema, sem categoria de side-effect, a skill nem entra no registry."*

### Optional: live failure

If time permits, switch to a branch with a deliberately broken skill:

```powershell
git checkout demo/broken-skill
uv run pytest tests/test_governance.py -v
```

Expected output (paraphrased):

```
FAILED tests/test_governance.py::test_skill_has_complete_manifest[bad_skill]
- AssertionError: bad_skill has no owner; refusing to register
```

Say:

> *"essa skill nem entra. O CI rejeita. A barreira não é técnica, é social —
> mas o teste é técnico."*

Switch back: `git checkout main`.

## Return-to-deck cue

> *"Voltando para a apresentação. A última peça é a mais importante: por
> que isso muda o que a gente discute em comitê?"*

## Fallback

1. Show `presentation/_fallback/pytest-governance.txt` — pre-captured output.
2. Read the test names aloud from the text file. The names are the point.
