# Anti-patterns

Four shapes I keep finding in enterprise codebases. Naming them is half
the fight.

## Vanity agent

> "We need a Marketing AI Agent." → "Why?" → "Because Sales has one."

The Marketing AI Agent inevitably ends up implementing the same five
skills the Sales one already has, with slightly different wording. The
real cost is not the model spend. It is the second policy review, the
second permission table, the second audit trail that nobody links to
the first.

**The fix** — show the requestor the existing agent's tool list. Often
the conversation ends there: *"oh, we already have all of these."*

## Skill-shaped agent

A team calls something "the X Agent" but when you open it, there is no
model call. It is a function with parameters that happens to live in the
agent platform because that is where new things land.

**The fix** — promote it to a real skill in the registry. Register it.
Version it. The "agent" disappears and the capability becomes a
first-class registered tool other agents can call.

## Orchestrator-shaped skill

A skill that "fetches data from API, formats it for the model, writes it
back to a database, and returns a status." This is three skills wearing
one hat: a query skill, a transformation skill, and a write skill.

**The fix** — split. Each piece gets its own owner, its own schema, and
its own audit trail. The orchestrator composes them. The orchestrator
gets shorter, not longer.

## Silent retry

A skill catches a transient downstream failure, sleeps two seconds,
retries, and returns `OK` regardless. The agent never learns there was
a problem. The caller cannot distinguish "succeeded on first try" from
"succeeded after three retries that took eight seconds."

**The fix** — return `TEMPORARY_FAILURE`. The orchestrator decides
whether to retry. The retry is recorded in evidence as a separate trace
with the same correlation id. Now the SRE can see the curve.

## Fat manifest

A skill manifest with a 600-character description that tries to teach
the model how to use the tool. The reason the description is long is
that the skill does multiple things.

**The fix** — split the skill. Each one earns a 60-character description
that fits in a Foundry tool list without scrolling. If your team cannot
write a 60-character description, the skill is doing too much.

## "We need an agent for that" reflex

The reflex appears every time a new capability is requested. A user
asks: *"can we summarize the policy in plain Portuguese?"* and the team
says *"we will build a Policy Summary Agent."*

**The fix** — that is not an agent. It is a `policy_summarize` skill
with a model call inside. Add it to the registry. Let existing agents
discover it. No agent definition required.

## "Each team owns its agent" governance

Every team gets to ship its own agent, its own skills, and its own
prompt. The registry is duplicated three times because each team forked
"to move faster." Within a year there are three `permission_check`
implementations with three different answers for the same actor.

**The fix** — one registry. Many consumers. Skills can be owned by
different teams as long as they are in the **same** registry. Ownership
is a manifest field, not a fork point.

## How to spot the patterns in committee

| Phrase you hear | Probable pattern |
|------------------|------------------|
| "We need an agent for [area]" | Vanity agent |
| "We are calling it an agent for now" | Skill-shaped agent |
| "It does several things in one call" | Orchestrator-shaped skill |
| "We added a retry inside the tool" | Silent retry |
| "The description got long" | Fat manifest |
| "Each team is faster owning their own" | Forked-registry governance |

Name the pattern in the room. Almost always, the room will let you fix it.
