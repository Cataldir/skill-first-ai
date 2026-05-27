# Infra

Two deployment paths supported. Pick one. Both honor the talk's argument:
tools sit behind a gateway, the agent sits in Foundry, neither owns the
other.

## Path A — APIM AI Gateway + Foundry prompt agent (default)

The MCP server is deployed to Azure Container Apps (or Azure Functions).
APIM AI Gateway publishes it as an MCP source. Foundry prompt agent
consumes the source.

See [`azd-init.md`](./azd-init.md) for the `azd up` walkthrough and
[`foundry.bicep`](./foundry.bicep) for the minimal IaC.

```
┌──────────────┐    ┌────────────┐    ┌────────────────────┐    ┌──────────────────┐
│   Foundry    │ -> │   APIM     │ -> │   Container Apps   │ -> │ skill registry   │
│ prompt agent │    │ AI Gateway │    │ (uvicorn MCP HTTP) │    │ (in-process)     │
└──────────────┘    └────────────┘    └────────────────────┘    └──────────────────┘
```

## Path B — Foundry Hosted Agent (containerized orchestrator)

The same Python package, wrapped in a container, registered as a Foundry
Hosted Agent. Skills run inside the container; no separate MCP server.

```
┌────────────────────────────────┐    ┌────────────────────┐
│ Foundry Hosted Agent (ACR)     │ -> │ Skill registry +   │
│ orchestrator: thin Python      │    │ direct calls       │
│ exposes: POST /invoke          │    │ (same package)     │
└────────────────────────────────┘    └────────────────────┘
```

A minimal Dockerfile lives at `infra/Dockerfile`. Use only if the team
explicitly wants the orchestrator to live in Foundry rather than behind
the gateway.

## Decision in one sentence

If you ask *"do we need control over the orchestrator process?"* and the
honest answer is no, use Path A. It is shorter, cheaper, and easier to
govern. Path B is for teams that already have a hosted-agent operational
model and want this code inside it.
