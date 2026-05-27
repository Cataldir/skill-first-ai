# Deploying to Microsoft Foundry

Two supported paths. Pick one for the demo; both are honest.

## Path A — Prompt agent + APIM-fronted MCP server (recommended for the demo)

This is the **shortest path** from `git clone` to a working Foundry agent.
It also separates concerns the way the talk argues for: tools live behind a
gateway, the agent lives in Foundry, and neither side owns the other.

### 1. Run the MCP server locally

```powershell
uv sync
uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080 --reload
```

Sanity check: `curl http://localhost:8080/mcp/tools` should list six tools.

### 2. Expose it through APIM AI Gateway

In the Azure portal:

1. Open APIM AI Gateway → **Workspaces & Tools**.
2. **Add tool** → MCP → point at `http://<public-url>:8080/mcp/tools`.
3. Apply the following policies (APIM templates exist for all of them):
   - JWT validation against the agent's Entra Agent Identity.
   - Per-skill rate limits — `ticket_open` is far more constrained than
     `policy_lookup`.
   - Token-limit policy with content-safety check for free-form fields.
4. Copy the published MCP URL and the API key.

### 3. Register the prompt agent in Foundry

1. Foundry → **Agents** → **New prompt agent**.
2. Paste the contents of `src/skill_first_ai/foundry/agent_definition.yaml`.
3. In Foundry secrets, add `skill-first-mcp-key` with the APIM API key.
4. Set environment variable `SKILL_FIRST_MCP_URL` to the APIM URL.
5. Use the inline `evals` block as the first eval set before promotion.

### 4. Demo

Open the Foundry chat playground for the registered agent and ask:

> Quero pedir reembolso de uma viagem de USD 1800 para um cliente novo.

You will see, in order, the tool calls `policy_lookup`, `permission_check`,
`document_search`, `justification_draft`, `ticket_open`, `evidence_log`,
each with its trace.

## Path B — Hosted Agent (containerized orchestrator)

Use this only if the team prefers the orchestrator code to live inside
Foundry. Same skills, same contract — only the boundary moves.

1. Build the container (`linux/amd64`, public ACR endpoint):

   ```powershell
   az acr build --registry <acr-name> --image skill-first-ai:1.0.0 .
   ```

2. Register as a Hosted Agent in Foundry, pointing at the ACR image and
   exposing port `8080`.
3. Wire the same APIM secret and MCP URL as environment variables.
4. The same `agent_definition.yaml` (without the `tools` block) becomes
   the system prompt; the orchestrator inside the container makes the
   skill calls directly.

If you find yourself reaching for Path B because "we need more control,"
re-read the talk. The likely answer is that you are missing a skill, not
that you need a custom container.
