# Demo 1 · Foundry portal · finance-orchestrator

**Slide cue**: slide 6.
**Target duration**: ~3 minutes.
**Goal**: prove the agent has no custom code — it is six MCP tools wired in.

## Steps

1. Open Foundry portal → Agents → `finance-orchestrator`.
2. Click **Configure**. Point at the **Tools** panel.
   - Six tools, all from MCP source `skill-first-mcp`.
   - Names exactly as registered: `policy_lookup`, `permission_check`,
     `document_search`, `justification_draft`, `ticket_open`, `evidence_log`.
3. Open the **Playground**. Clear any prior conversation.
4. Type, slowly, in PT-BR:
   > Quero solicitar reembolso de USD 1800 de uma viagem para visitar um cliente novo.
5. Pause before sending. Say to the room:
   > *"Vocês vão ver seis tool calls, nessa ordem."*
6. Send. Watch the tool call trace appear.
7. Read each call aloud as it lands:
   - `policy_lookup(topic="expense.travel")` → returns the USD 1500 rule.
   - `permission_check(actor=..., permission="expense.submit")` → allowed.
   - `document_search(query="travel policy expense")` → three docs.
   - `justification_draft(...)` → composed text.
   - `ticket_open(...)` → `TCK-XXXXXXXX`.
   - `evidence_log(...)` → recorded with matching correlation id.
8. Open one trace. Show `correlation_id`, `skill_name`, `skill_version`,
   `latency_ms`, `category`.

## Return-to-deck cue

> *"Voltando para a apresentação. A pergunta agora é: o que faz aquelas
> seis ferramentas serem reutilizáveis?"*

## Fallback

If Foundry lags or fails:

1. Switch to `presentation/_fallback/foundry-finance-trace.png` fullscreen.
2. Walk the trace verbally using the screenshot as your reference.
3. Say: *"o Foundry está com lag — mas o trace aparece exatamente assim."*
4. Advance to the next slide. Do not retry live.
