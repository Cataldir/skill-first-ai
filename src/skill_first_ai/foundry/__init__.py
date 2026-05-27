"""Foundry integration surfaces.

Two ways the registry reaches Microsoft Foundry, both honored:

- ``mcp_server`` — a FastAPI app that publishes every registered skill
  as an MCP tool. Sits behind APIM AI Gateway and is consumed by Foundry
  prompt agents.
- ``agent_definition.yaml`` — the Foundry prompt-agent definition that
  loads those tools and produces the live demo flow.

The Hosted Agent path is documented in ``deploy.md``: the same Python
package is wrapped in a container and registered as a Foundry Hosted
Agent if a team wants the orchestrator itself to live inside Foundry.
"""
