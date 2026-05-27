# Demo · Intro

This folder mirrors `docs/05-demo-script.md` as four printable cue cards
sized for stage use. One file per demo segment.

## Setup checklist

- [ ] `uv sync`
- [ ] `uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080`
- [ ] Public tunnel pointing at port 8080 (`ngrok http 8080` or `devtunnel host -p 8080 -a`)
- [ ] APIM AI Gateway MCP source updated to tunnel URL
- [ ] Foundry portal: finance and HR agents pre-loaded in separate tabs
- [ ] Slides in Marp preview at fullscreen
- [ ] `_fallback/` screenshots ready
- [ ] `pytest -v` green
- [ ] Laptop on power, second monitor for cue cards

## Demo order

1. [`01-foundry-portal-tour.md`](./01-foundry-portal-tour.md)
2. [`02-skill-as-mcp-tool.md`](./02-skill-as-mcp-tool.md)
3. [`03-governance-tests.md`](./03-governance-tests.md)
4. [`04-second-agent-reuse.md`](./04-second-agent-reuse.md)

Each demo ends by returning to the deck. Honor the cue.
