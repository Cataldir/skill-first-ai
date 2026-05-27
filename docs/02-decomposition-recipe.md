# Decomposition recipe

Most "agent for X" requests are workflows with a missing capability list.
This recipe is how to find the capabilities before you build the agent.

## Step 0 — Write the user sentence

A single sentence in the user's voice. No marketing copy. No "AI-powered."

> *"Quero pedir reembolso de uma viagem de USD 1800 para visitar um cliente novo."*

If you cannot write this sentence, the agent has no concrete job. Stop here.

## Step 1 — List the questions the system must answer

For the sentence above:

1. What does our policy say about travel above USD 1500?
2. Does this user have permission to submit this expense?
3. Where is the supporting documentation (policy PDF, prior approvals)?
4. What is the justification we will record for this approval?
5. Where do we open the actual ticket?
6. How do we record evidence that this happened?

Six questions. Each one is a capability.

## Step 2 — Name each capability with a verb + noun

| Question | Skill |
|----------|-------|
| What does policy say? | `policy_lookup` |
| Does the user have permission? | `permission_check` |
| Where is the documentation? | `document_search` |
| What is the justification? | `justification_draft` |
| Where do we open the ticket? | `ticket_open` |
| How do we record evidence? | `evidence_log` |

Names are stable, lower-snake-case, and bilingual-friendly. The agent's
system prompt references the same names — that is the wiring.

## Step 3 — Check for reuse first

Before you implement a new skill, search the registry:

```python
from skill_first_ai.registry import default_registry
for skill in default_registry():
    print(skill.manifest.name, skill.manifest.version, skill.manifest.description)
```

If a capability already exists, you do not write it again. You **call** it.
This is the only rule that prevents skill sprawl.

## Step 4 — Decide the contract before the implementation

For each new skill, write the manifest and schemas first:

```python
class PolicyLookupInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    topic: str = Field(description="Dotted topic, e.g. expense.travel")

class PolicyLookupOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    topic: str
    summary: str
    owner: str
    last_reviewed: str

manifest = SkillManifest(
    name="policy_lookup",
    version="1.0.0",
    description="Return the canonical policy snippet for a topic.",
    owner="Finance Operations",
    tags=("policy", "knowledge"),
    side_effects=False,
    pii=False,
)
```

The contract review (owner + description + side-effects + PII) happens
**before** the implementation. If owner approval is unclear, the skill
does not get coded yet.

## Step 5 — Implement `_execute`

```python
class PolicyLookup(BaseSkill[PolicyLookupInput, PolicyLookupOutput]):
    InputSchema = PolicyLookupInput
    OutputSchema = PolicyLookupOutput
    manifest = manifest

    def _execute(self, payload: PolicyLookupInput) -> PolicyLookupOutput:
        record = lookup(payload.topic)
        if record is None:
            raise InvalidInputError(f"unknown policy topic: {payload.topic!r}")
        return PolicyLookupOutput(...)
```

Three rules:

- Raise typed errors — `InvalidInputError`, `SkillRefused`, `TransientSkillError`.
- Never return None. Either the OutputSchema or raise.
- Never log secrets in the message; the message is exposed to the agent.

## Step 6 — Register

In `registry/registry.py::default_registry()`:

```python
registry.register(PolicyLookup())
```

That is the only place skills become visible to agents.

## Step 7 — Write the orchestrator (the boring part)

The orchestrator imports the **registry**, not the skills:

```python
@dataclass(frozen=True)
class FinanceAgent:
    registry: SkillRegistry

    def handle(self, request: FinanceRequest) -> FinanceResponse:
        policy = self._call("policy_lookup", {"topic": request.policy_topic})
        if policy.category is not ResultCategory.OK:
            return self._refuse(policy, ...)
        ...
```

The orchestrator is short. The decision logic is in the skills + categories.
If your orchestrator grows past 200 lines, you have inlined capability
logic that should be a skill.

## Step 8 — Expose to Foundry

The MCP server in `foundry/mcp_server.py` publishes the entire registry
without any per-skill code. The Foundry prompt agent definition
(`foundry/agent_definition.yaml`) references the same names.

Adding a skill does not require touching the MCP server. It does not
require touching the agent definition unless you want the agent to use it.

## The recipe in one paragraph

Write the user sentence. List the questions. Name the verbs. Check the
registry. Write the contract. Get owner approval. Implement `_execute`.
Register. Compose. Expose. **No new agent unless the registry is missing
a capability the new agent needs.**
