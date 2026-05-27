# Demo 4 · Second agent · hr-orchestrator

**Slide cue**: slide 13.
**Target duration**: ~2 minutes.
**Goal**: show that the same six skills back a second agent. No new code,
no new MCP source, no new infrastructure.

## Steps

1. Switch to the Foundry tab with `hr-orchestrator`.
2. Click **Configure**. Show the **Tools** panel.
   - Same six tools, **same names**, same MCP source.
   - The only thing different is the system prompt.
3. Open the **Playground**. Type, slowly:
   > Quero solicitar 18 dias de férias em julho.
4. Send. Watch the trace.
   - `policy_lookup(topic="hr.vacation")` → returns the 15-day rule.
   - `permission_check(actor=..., permission="hr.vacation.request")` → allowed.
   - `document_search(query="vacation HR leave")` → finds the form.
   - `justification_draft(...)` → composed text.
   - `ticket_open(category="hr", ...)` → `TCK-XXXXXXXX`.
   - `evidence_log(...)` → recorded.
5. Say:
   > *"mesma sequência. As skills são iguais. A política e a permissão é
   > que mudam. Foi isso o trabalho do RH no primeiro dia: escrever o
   > system prompt. Não escrever as ferramentas."*

## Return-to-deck cue

> *"Voltando para a apresentação para fechar. A última pergunta é a que
> mais incomoda em comitê."*

## Fallback

1. Show `presentation/_fallback/foundry-hr-trace.png` fullscreen.
2. Read the trace aloud from the screenshot.
3. Say the same line:
   > *"mesma sequência, política e permissão diferentes, skills iguais."*
