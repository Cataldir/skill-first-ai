"""FastAPI server that exposes every registered skill through FastAPI-MCP.

Run locally with::

    uv run uvicorn skill_first_ai.foundry.mcp_server:app --port 8080

Then point your Foundry prompt agent at ``http://localhost:8080/mcp``.
FastAPI-MCP mounts the real MCP HTTP transport at that path and turns the
six typed skill endpoints below into MCP tools.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel

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


def _skill_result_payload(result: Any) -> dict[str, Any]:
    return {
        "category": result.category.value,
        "output": (
            result.output.model_dump(mode="json") if result.output is not None else None
        ),
        "message": result.message,
        "trace": result.trace.model_dump(mode="json"),
    }


def _invoke_skill(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    registry = _registry()
    try:
        skill = registry.get(name)
    except UnknownSkillError as exc:
        raise HTTPException(status_code=404, detail=f"unknown skill: {name}") from exc

    correlation_id = payload.pop("__correlation_id", None)
    result = skill.run(payload, correlation_id=correlation_id)
    return _skill_result_payload(result)


def _make_tool_endpoint(name: str) -> Callable[[BaseModel], dict[str, Any]]:
    async def endpoint(payload: BaseModel) -> dict[str, Any]:
        return _invoke_skill(name, payload.model_dump(mode="json"))

    return endpoint


def _register_tool_endpoints() -> list[str]:
    operation_ids: list[str] = []
    for skill in _registry():
        endpoint = _make_tool_endpoint(skill.manifest.name)
        endpoint.__name__ = skill.manifest.name
        endpoint.__doc__ = skill.manifest.description
        endpoint.__annotations__ = {
            "payload": skill.InputSchema,
            "return": dict[str, Any],
        }
        app.post(
            f"/api/tools/{skill.manifest.name}",
            operation_id=skill.manifest.name,
            tags=["mcp-skill"],
            summary=skill.manifest.description,
        )(endpoint)
        operation_ids.append(skill.manifest.name)
    return operation_ids


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
    return _invoke_skill(name, payload)


MCP_TOOL_OPERATION_IDS = _register_tool_endpoints()
mcp = FastApiMCP(
    app,
    name="skill-first-ai",
    description="MCP server for the skill-first AI demo registry.",
    include_operations=MCP_TOOL_OPERATION_IDS,
    describe_full_response_schema=True,
    describe_all_responses=True,
)
mcp.mount_http(mount_path="/mcp")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
