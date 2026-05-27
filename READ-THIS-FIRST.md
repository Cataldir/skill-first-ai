# Read-this-first · Dengo / TDC AI Tech Circle

**Date**: 28 May 2026.
**Audience**: ~38 senior leaders. B3, Bradesco, BV, BB, BTG, Pan, Safra,
Braskem, CPFL, Fiesp, Interplayers, Itaú, PAGBANK, Petrobras, Prodesp,
SENAI-SP, SESI-SP, Stone, UOL, XP.
**Format**: 25–30 min talk + 10–15 min Q&A.
**Argument in one line**: most enterprise "agent strategies" are six
redundant chatbots in a trench coat — the real unit is the reusable
skill behind a typed contract.

## Where the repo lives right now

This staging copy: `c:\Users\ricar\Github\i\tmp\skill-first-ai-dengo\`.
**Move it** to its real home before tomorrow:

```powershell
Move-Item `
  "C:\Users\ricar\Github\i\tmp\skill-first-ai-dengo" `
  "C:\Users\ricar\Github\skill-first-ai"
```

Full push instructions: [`push-to-github.md`](./push-to-github.md).
Target repo: `https://github.com/Cataldir/skill-first-ai` (public).

## Final state — what is in the box

- ✅ **40 / 40 tests passing** (unit + governance + orchestrator).
- ✅ **MCP server boots** and serves 6 tools on `/mcp/tools`.
- ✅ **FinanceAgent runs end-to-end**, emits ticket + 6 traces.
- ✅ **HR agent definition** (`src/skill_first_ai/foundry/hr_agent_definition.yaml`)
  shares all 6 skills with the finance agent.
- ✅ **Marp deck** (17 slides, PT-BR, brand palette) + speaker notes.
- ✅ **4 demo cue cards** for the segmented Foundry ↔ repo ↔ slides flow.
- ✅ **Infra**: minimal Bicep + azd walkthrough + Dockerfile (Path B).
- ✅ **6 docs** (vocabulary, contract, recipe, governance, anti-patterns, demo script).

## Tonight's checklist (before sleeping)

1. Move the folder out of `tmp/` (command above).
2. Run `push-to-github.md` end-to-end.
3. Visit `https://github.com/Cataldir/skill-first-ai` and confirm the
   README renders cleanly.
4. Build the deck locally:
   ```powershell
   npx @marp-team/marp-cli@latest presentation/slides.md --pdf --allow-local-files
   ```
   Verify the brand colors render correctly.
5. Pre-capture the four fallback screenshots into
   `presentation/_fallback/`:
   - `foundry-finance-trace.png` (Demo 1)
   - `vscode-skill-contract.png` (Demo 2)
   - `pytest-governance.txt` (Demo 3)
   - `foundry-hr-trace.png` (Demo 4)
6. Re-read `presentation/speaker-notes.md` once. Note the return-to-deck
   cues — those are the seams that hold the segmented demo together.

## Morning checklist (90 min before)

1. Laptop on power, second monitor for cue cards.
2. Foundry portal open in two tabs:
   - Tab 1: `finance-orchestrator` agent, Playground ready.
   - Tab 2: `hr-orchestrator` agent, Playground ready.
3. Terminal at repo root, three panes:
   - Pane A: `uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080`
   - Pane B: `ngrok http 8080` (or `devtunnel host -p 8080 -a`)
   - Pane C: empty, ready for `uv run pytest tests/test_governance.py -v`
4. APIM AI Gateway MCP source set to the tunnel URL (test by sending one
   request from Foundry playground first).
5. Marp preview in fullscreen on the projector output.
6. Demo cue cards (`demo/*.md`) printed or open on the second monitor.
7. Phone on silent. Bottle of water.

## The voice test, last call

The deck and the README should pass all five gates:

1. Friction line in the first 80 chars? Yes — "seis chatbots redundantes
   num casaco só."
2. Mechanism beat after the friction? Yes — the six-skill decomposition.
3. Punchline that earns the smile? Yes — "antes de criar um agente
   financeiro, escreva a frase do usuário."
4. Could anyone at Microsoft, AWS, or Google have written this? No —
   specific examples, specific Foundry vocabulary, specific Brazilian
   audience cues in the notes.
5. Specific named thing? Yes — APIM AI Gateway, Foundry prompt agents,
   `SkillResult` envelope, the six named skills.

## Cut-line if you run long

If you hit slide 11 (governance pytest demo) and you have less than 8
minutes left:

- Skip Demo 3 (pytest). Say:
  > *"O teste de governança está no repositório, em
  > `tests/test_governance.py`. Roda em 0,5 segundos."*
- Go straight to Slide 12 (reuse), do Demo 4 (HR agent in Foundry).
- Close on Slides 14–16. Do not cut the closing.

## Cut-line if Foundry breaks

If Foundry is down or APIM is misbehaving:

- Skip Demo 1 and Demo 4 entirely. Use screenshots in `_fallback/`.
- Lean harder on Demo 2 (VS Code repo walkthrough) and Demo 3 (pytest).
- The argument still works — it just lands as code-first instead of
  portal-first.

## What I would *not* improvise

- The pergunta-honesta slide (slide 2). It is the doorway.
- The decomposition table (slide 5). It is the proof.
- The "uma skill, dois agentes" demo cue (slide 13). It is the payoff.
- The closing line on slide 16. Not negotiable.

Everything else, you can compress, expand, or skip. Those four are the spine.

---

Boa apresentação. Make the room argue about the right thing.
