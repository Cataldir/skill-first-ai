"""FastAPI/FastMCP server that exposes every registered skill as an MCP tool.

Run locally with::

    uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080

Then point your Foundry prompt agent at ``http://localhost:8080/mcp``
through APIM AI Gateway (or expose directly during demos).

Why FastAPI instead of FastMCP directly: FastAPI is the most portable
HTTP surface and Foundry's MCP client speaks plain HTTP to the gateway
just fine. Production swaps the transport, not the skill code.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException

from skill_first_ai.registry.registry import (
    SkillRegistry,
    UnknownSkillError,
    default_registry,
)

app = FastAPI(
    title="Skill-first AI MCP Server",
    description=(
        "Exposes the canonical skill registry as MCP-compatible HTTP tools. "
        "Every endpoint is one skill. Same registry as the Python orchestrator."
    ),
    version="1.0.0",
)


def _registry() -> SkillRegistry:
    # Cached on app.state so each request reuses the same registry.
    if not hasattr(app.state, "registry"):
        app.state.registry = default_registry()
    return app.state.registry  # type: ignore[no-any-return]


@app.get("/mcp/tools", tags=["mcp"])
def list_tools() -> dict[str, Any]:
    """List skills as MCP tool definitions: name, description, JSON schema.

    The Foundry prompt agent reads this list to populate its tool palette.
    """
    registry = _registry()
    tools = []
    for skill in registry:
        tools.append(
            {
                "name": skill.manifest.name,
                "version": skill.manifest.version,
                "description": skill.manifest.description,
                "input_schema": skill.InputSchema.model_json_schema(),
                "output_schema": skill.OutputSchema.model_json_schema(),
                "side_effects": skill.manifest.side_effects,
                "requires_approval": skill.manifest.requires_approval,
                "owner": skill.manifest.owner,
                "tags": list(skill.manifest.tags),
            },
        )
    return {"tools": tools}


@app.post("/mcp/tools/{name}", tags=["mcp"])
def call_tool(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Invoke a skill by name. Returns the SkillResult envelope verbatim.

    No extra wrapping — Foundry sees ``category``, ``output``, ``message``,
    and ``trace`` exactly as the Python caller does. That is the point
    of having one contract.
    """
    registry = _registry()
    try:
        skill = registry.get(name)
    except UnknownSkillError as exc:
        raise HTTPException(status_code=404, detail=f"unknown skill: {name}") from exc

    correlation_id = payload.pop("__correlation_id", None)
    result = skill.run(payload, correlation_id=correlation_id)
    return {
        "category": result.category.value,
        "output": (
            result.output.model_dump() if result.output is not None else None
        ),
        "message": result.message,
        "trace": result.trace.model_dump(),
    }


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
