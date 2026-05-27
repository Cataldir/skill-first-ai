# `azd up` walkthrough

For the day-of-demo deployment. Use only if the local + ngrok path is
not feasible at the venue.

## Prereqs

- Azure subscription with Foundry project already created.
- `azd` (Azure Developer CLI) installed.
- A Container Registry (or use Azure's `acr build` shortcut).
- APIM AI Gateway service available in the subscription (or provisioned
  by this template — note that APIM takes ~30 minutes the first time).

## One-time setup

```powershell
# from repo root
azd auth login
azd init --template . --environment skill-first-aitc
```

When prompted, set:

- `AZURE_LOCATION` → `eastus2` (or your preferred Foundry region).
- `AZURE_RESOURCE_GROUP` → `rg-skill-first-aitc`.

## Build the image

```powershell
az acr build `
  --registry <your-acr-name> `
  --image skill-first-ai:1.0.0 `
  --file infra/Dockerfile .
```

## Provision and deploy

```powershell
azd provision `
  --output json `
  -e skill-first-aitc
```

This deploys [`infra/foundry.bicep`](./foundry.bicep). Read the JSON output
for `mcpUrl` and `apimGatewayUrl`.

## Register in APIM AI Gateway

The MCP source registration is portal-driven (see notes in `deploy.md`):

1. Azure portal → APIM AI Gateway → **Workspaces & Tools**.
2. **Add tool** → MCP → URL = `mcpUrl` from the azd output + `/tools`.
3. Apply policies:
   - JWT validation against the agent's Entra Agent Identity.
   - Per-skill rate limits.
   - Content-safety check on free-text inputs.
4. Copy the published MCP URL — this is what Foundry consumes.

## Register the Foundry agent

In Foundry portal:

1. Agents → **New prompt agent**.
2. Paste `src/skill_first_ai/foundry/agent_definition.yaml`.
3. Set `SKILL_FIRST_MCP_URL` to the APIM gateway URL.
4. Set secret `skill-first-mcp-key`.
5. Save. Open the playground. Run the demo prompt.

## Teardown

```powershell
azd down --purge -e skill-first-aitc
```

APIM Developer SKU takes ~10 minutes to fully delete. Run teardown the
evening after the talk, not five minutes after.

## Notes

- The Bicep does not provision the Foundry project — it assumes an
  existing one. If you do not have one yet, create it via
  `az cognitiveservices account create` with `--kind AIServices`.
- The Container App ingress is set to external for demo speed. In
  production, keep it internal and reach it from APIM via VNet integration.
- The image must be built for `linux/amd64`. If you build on Apple
  Silicon, pass `--platform linux/amd64` to `docker buildx`.
