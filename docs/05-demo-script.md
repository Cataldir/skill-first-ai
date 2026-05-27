# Demo script — segmented flow

Same content as the speaker notes, condensed and reorderable. Use this
as the printed cue card on stage.

## Slide 6 — Demo 1 · Foundry portal · finance-orchestrator (~3 min)

1. Foundry → Agents → `finance-orchestrator` → Configure.
2. Show **Tools** panel — six MCP tools from `skill-first-mcp`.
3. Playground. Type, slowly:
   > Quero solicitar reembolso de USD 1800 de uma viagem para visitar um cliente novo.
4. Watch the tool call trace: `policy_lookup` → `permission_check` →
   `document_search` → `justification_draft` → `ticket_open` → `evidence_log`.
5. Comment each call by name. Point at the trace IDs.
6. **Return to the deck.** Cue: *"Voltando para a apresentação."*

## Slide 9 — Demo 2 · Repo (~3 min)

1. VS Code → `src/skill_first_ai/contracts/skill.py` → highlight `BaseSkill.run`.
2. Open `src/skill_first_ai/skills/policy_lookup.py` → highlight `_execute`.
3. Open `src/skill_first_ai/registry/registry.py` → highlight `default_registry()`.
4. Open `src/skill_first_ai/foundry/mcp_server.py` → highlight `list_tools` and `call_tool`.
5. **Return to the deck.** Cue: *"Voltando para a apresentação."*

## Slide 11 — Demo 3 · Governance pytest (~2 min)

1. Terminal large. From repo root:
   ```powershell
   uv run pytest tests/test_governance.py -v
   ```
2. Read test names aloud as they pass.
3. Optional: switch to branch `demo/broken-skill` and re-run to show CI rejection.
4. **Return to the deck.** Cue: *"Voltando para a apresentação."*

## Slide 13 — Demo 4 · Foundry portal · hr-orchestrator (~2 min)

1. Foundry → Agents → `hr-orchestrator` → Configure.
2. Show **Tools** panel — *same six* MCP tools, different system prompt.
3. Playground. Type, slowly:
   > Quero solicitar 18 dias de férias em julho.
4. Same tool call trace shape. Different policy and permission. Same skills.
5. **Return to the deck.** Cue: *"Voltando para a apresentação para fechar."*

## Cold-start kit (the morning of)

- `uv sync` clean.
- `uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080`.
- ngrok or dev tunnel pointing port 8080 to public URL.
- APIM AI Gateway MCP source updated to that URL.
- Foundry: open finance and HR agents in two tabs, **already loaded**.
- Slides in Marp preview, fullscreen on projector.
- Fallback screenshots in `presentation/_fallback/`.
- Pytest green.

## Hard-rule

Every demo ends by returning to the slide before moving forward.
The slide is the guide. The demo is the punchline.
