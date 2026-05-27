# skill-first-ai

> Fewer agents, more reusable capabilities.
> A reference implementation for skill-first AI on Microsoft Foundry.

Most enterprise agent strategies are six redundant chatbots in a trench coat.
The HR agent, the finance agent, the legal agent, the IT agent, the customer
service agent, the procurement agent — each one re-implementing the same five
things from a slightly different prompt, each one storing its own version of
"how access works at this company," none of them auditable in the way the
risk team actually needs.

This repo argues for the other shape. Before you ship one more agent, you ship
the capabilities the agent would have called: consult policy, check permission,
search documents, open a ticket, log evidence, draft a justification. Six small
skills, owned by humans, versioned, tested, governed once. Then the agent is the
boring part — a prompt that composes them.

It is the same argument I keep making in posts like
[*Tool calling is not architecture*][tool-calling] and [*Beyond chatbots:
patterns for agentic systems on Microsoft Foundry*][beyond-chatbots]. The point
of this repo is that those posts now have running code attached.

[tool-calling]: https://medium.com/@cataldi.ricardo/tool-calling-is-not-architecture
[beyond-chatbots]: https://medium.com/@cataldi.ricardo/beyond-chatbots-patterns-for-agentic-systems-on-microsoft-foundry

## What is inside

```
skill-first-ai/
├── src/skill_first_ai/
│   ├── contracts/skill.py         # The skill contract everyone honors
│   ├── skills/                    # Six concrete, reusable skills
│   ├── registry/registry.py       # The single registry, by name+version
│   ├── orchestrator/finance_agent.py  # A thin agent that composes skills
│   └── foundry/
│       ├── mcp_server.py          # Exposes the registry as MCP tools
│       ├── agent_definition.yaml  # The Foundry prompt agent
│       └── deploy.md              # APIM AI Gateway + Hosted Agent paths
├── tests/
│   ├── test_skills_unit.py        # Behavior per skill
│   ├── test_governance.py         # The contract: owner, schema, side-effects
│   └── test_orchestrator.py       # End-to-end refusal and approval flows
├── docs/                          # Vocabulary, recipe, governance, anti-patterns
├── demo/                          # Segmented demo cue cards
├── presentation/                  # Marp deck, PT-BR, with speaker notes
└── infra/                         # azd-init notes and minimal Bicep
```

## The five-minute version

```powershell
git clone https://github.com/Cataldir/skill-first-ai.git
cd skill-first-ai
uv sync
uv run pytest -v
uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080
```

Then `curl http://localhost:8080/mcp/tools` and watch every registered skill
publish its JSON schema. Register that URL in Foundry as an MCP source, paste
[`src/skill_first_ai/foundry/agent_definition.yaml`][agent] into a new prompt
agent, and the finance orchestrator is live.

The same six tools back the HR agent and the IT agent. That is the whole point.

[agent]: ./src/skill_first_ai/foundry/agent_definition.yaml

## The skill contract

```python
class BaseSkill(abc.ABC, Generic[InputT, OutputT]):
    manifest: ClassVar[SkillManifest]
    InputSchema: ClassVar[type[BaseModel]]
    OutputSchema: ClassVar[type[BaseModel]]

    def run(self, payload, *, correlation_id=None) -> SkillResult: ...
```

Four jobs, in order: identity, translation, failure, evidence.

- *Identity* — a stable name and semantic version every caller can pin.
- *Translation* — Pydantic schemas convert whatever the agent sent into a typed
  domain model before any side effect runs.
- *Failure* — `ResultCategory.OK | INVALID_INPUT | REFUSED | TEMPORARY_FAILURE`.
  No exception-throwing in the agent's hot path; every business outcome has a
  named category.
- *Evidence* — every call emits a frozen `SkillTrace` with correlation ID,
  skill name, version, latency, and category. Auditors do not have to guess.

That contract is the only thing that matters. The MCP server, the FastAPI
wrapper, the Hosted Agent option, and direct Python imports all return the
same `SkillResult` envelope.

## Demo flow

This repo is the companion to a talk delivered to a group of Brazilian C-level
leaders ([Dengo / TDC AI Tech Circle, May 28 2026][talk-meta]). The deck lives
in [`presentation/`][slides] and drives a segmented demo:

1. **Slides — set the question.** Why does every area think it needs its own agent?
2. **Foundry portal — show the prompt agent.** Six MCP tools wired in, no custom code.
3. **Slides — name the contract.** Identity, translation, failure, evidence.
4. **Repo docs — open the contract.** `BaseSkill`, `SkillManifest`, `ResultCategory`.
5. **Slides — show the recipe.** Finance agent decomposed into six skills.
6. **Repo + pytest — governance live.** `pytest tests/test_governance.py -v`.
7. **Foundry portal — the punchline.** Same six tools, swapped system prompt, the
   HR agent works.
8. **Slides — the central question.** *"A empresa precisa de mais agentes, ou de
   melhores capacidades reutilizáveis?"*

The slides are always the guide. The demos are short, named, and return to the
deck. The cue cards in [`demo/`][demo] are written for that pacing.

[talk-meta]: ./presentation/README.md
[slides]: ./presentation/slides.md
[demo]: ./demo/

## Why this matters

The teams I see drown in agents are not drowning in models. They are drowning in
duplicated capability-shaped code, each copy with slightly different policy,
slightly different permission logic, no shared audit trail, and a single
sentence in a chat log to explain a decision that touched USD 12k of spend.

The fix is not a smarter agent. The fix is a registry — boring, named,
versioned, tested — that the agents call. Once it exists, you can finally have
the conversation that matters: *do we need another agent, or do we need another
skill?*

This repo is one way to start that conversation with running code.

## Read next

- [`docs/00-vocabulary.md`](./docs/00-vocabulary.md) — agent / skill / workflow / automation
- [`docs/01-skill-contract.md`](./docs/01-skill-contract.md) — what the contract enforces
- [`docs/02-decomposition-recipe.md`](./docs/02-decomposition-recipe.md) — how to break a generic agent into capabilities
- [`docs/03-governance.md`](./docs/03-governance.md) — test, version, govern
- [`docs/04-anti-patterns.md`](./docs/04-anti-patterns.md) — vanity agents, redundant agents, skill-shaped agents
- [`presentation/speaker-notes.md`](./presentation/speaker-notes.md) — the segmented demo flow in detail

MIT licensed. Built around Microsoft Foundry. Maintained as a companion to my
public writing on agentic architectures.
