"""Tests for the FastAPI-MCP mounted server."""

from __future__ import annotations

from fastapi.testclient import TestClient

from skill_first_ai.foundry.mcp_server import MCP_TOOL_OPERATION_IDS, app, mcp


EXPECTED_TOOLS = {
    "document_search",
    "evidence_log",
    "justification_draft",
    "permission_check",
    "policy_lookup",
    "ticket_open",
}


def test_fastapi_mcp_mounts_http_endpoint_at_mcp():
    route_paths = {getattr(route, "path", None) for route in app.routes}

    assert "/mcp" in route_paths


def test_fastapi_mcp_exposes_exactly_six_skill_tools():
    assert set(MCP_TOOL_OPERATION_IDS) == EXPECTED_TOOLS
    assert {tool.name for tool in mcp.tools} == EXPECTED_TOOLS


def test_legacy_tool_catalog_still_returns_six_definitions():
    response = TestClient(app).get("/mcp/tools")

    assert response.status_code == 200
    tools = response.json()["tools"]
    assert len(tools) == 6
    assert {tool["name"] for tool in tools} == EXPECTED_TOOLS
    assert "input_schema" in tools[0]


def test_legacy_tool_call_still_invokes_skill():
    response = TestClient(app).post(
        "/mcp/tools/policy_lookup",
        json={"topic": "expense.travel"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "ok"
    assert payload["output"]["topic"] == "expense.travel"


def test_generated_fastapi_tool_endpoint_invokes_skill():
    response = TestClient(app).post(
        "/api/tools/policy_lookup",
        json={"topic": "expense.travel"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "ok"
    assert payload["output"]["topic"] == "expense.travel"
