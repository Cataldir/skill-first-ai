# Demo 2 · Repository · contract + MCP server

**Slide cue**: slide 9.
**Target duration**: ~3 minutes.
**Goal**: show the contract in code; prove that what Foundry showed is
the same Pydantic model that lives in the registry.

## Steps

1. VS Code → open `src/skill_first_ai/contracts/skill.py`.
   - Highlight `BaseSkill.run` — say:
     > *"esse método aqui é o único lugar onde tempo, erro e trace são montados."*
   - Highlight `ResultCategory` enum.
   - Highlight `SkillManifest` fields. Say:
     > *"se um desses campos não existe, a skill nem entra no registry."*
2. Open `src/skill_first_ai/skills/policy_lookup.py`.
   - Less than 100 lines.
   - Point at the `manifest`, the `_execute`, and the typed errors.
3. Open `src/skill_first_ai/registry/registry.py`.
   - Highlight `default_registry()`. Say:
     > *"se uma skill não está aqui, nenhum agente pode chamar. Toda a
     > governança começa nesse `register()`."*
4. Open `src/skill_first_ai/foundry/mcp_server.py`.
   - Highlight `list_tools` and `call_tool`.
   - Say:
     > *"o que o Foundry consome é exatamente isso. Não tem código duplicado
     > entre a skill e o tool MCP."*

## Return-to-deck cue

> *"Voltando para a apresentação. A próxima pergunta é: como a gente impede
> que essas skills virem bagunça em seis meses?"*

## Fallback

If VS Code refuses to cooperate:

1. Open `github.com/Cataldir/skill-first-ai/blob/main/src/skill_first_ai/contracts/skill.py` in a browser.
2. Same path, same talking points. Browser does not zoom as well — bump font in advance.
