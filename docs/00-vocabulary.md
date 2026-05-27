# Vocabulary

Most arguments about agent strategy fail because the four words below get
treated as synonyms. They are not. Each one demands a different level of
governance, a different deployment topology, and a different conversation
in a steering committee.

## Automation (traditional)

Deterministic flow. Branching rules. Robotic Process Automation. Excel macros.
n8n, Zapier, Power Automate flows without any LLM step.

- **What it is**: known inputs map to known outputs through fixed logic.
- **What it is not**: open-ended. It cannot handle a phrase it was not told to handle.
- **Governance need**: low. You can read the flow.

## Skill (capability)

A small, named, versioned, typed unit of capability. Has an explicit input schema,
an explicit output schema, and a `SkillManifest` that records owner, side-effects,
and PII class. Every call leaves a `SkillTrace`.

- **What it is**: a function with a contract and an audit trail.
- **What it is not**: a conversation. It does not talk to the user.
- **Governance need**: high — because every other layer reuses it.

> If it does not have a manifest, it is not a skill. It is a function
> someone gave a friendly name.

## Workflow

An *explicit* orchestration of skills. The control flow is visible in code
(state machine, BPMN, durable functions) and reviewable. Branches are named.

- **What it is**: a script that calls skills in a controlled order.
- **What it is not**: improvisation. A workflow does not "decide" mid-flight.
- **Governance need**: medium. Tested as a system.

## Agent

A composition of skills under model-driven control. The agent chooses
which skill to call, when, with what input, and how to react to refusals
and failures. It may carry memory. It may run multi-turn.

- **What it is**: the runtime that turns a user request into a chain of skill calls.
- **What it is not**: a place to put new capability logic. The agent picks; the skill does.
- **Governance need**: medium for prompt-only agents; high for tool-using agents
  that touch side effects. Largely **derived from the skills it can call**.

## When the words get mixed

| Symptom | Probable confusion | Fix |
|---------|---------------------|-----|
| "Our agent has a problem with policy lookup" | Skill-shaped logic living inside agent prompt | Move to a `policy_lookup` skill in the registry |
| "We need a workflow with AI in it" | Workflow that calls one skill that calls a model | Keep workflow explicit; do not let model run the branching |
| "Let's build an agent for invoice approval" | Workflow disguised as agent | Pick the cheapest shape that solves it; workflow if order is fixed |
| "Replace agent A with agent B" | Two agents share 80% of their skills | Reuse the registry; rewrite only the system prompt |

## The talk in one sentence

You almost never need another agent. You need another skill, or you need
to admit the skill you have already has the wrong contract.
