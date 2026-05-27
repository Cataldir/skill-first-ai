"""Unit tests for each skill. Verify the happy path and the documented
failure modes."""

from __future__ import annotations

import pytest

from skill_first_ai.contracts.skill import ResultCategory
from skill_first_ai.skills.document_search import DocumentSearch
from skill_first_ai.skills.evidence_log import EvidenceLog, evidence_dump, evidence_reset
from skill_first_ai.skills.justification import JustificationDraft
from skill_first_ai.skills.permission_check import PermissionCheck
from skill_first_ai.skills.policy_lookup import PolicyLookup
from skill_first_ai.skills.ticket_open import TicketOpen


def test_policy_lookup_returns_known_topic():
    result = PolicyLookup().run({"topic": "expense.travel"})
    assert result.category is ResultCategory.OK
    assert result.output is not None
    assert "director approval" in result.output.summary.lower()  # type: ignore[attr-defined]


def test_policy_lookup_rejects_unknown_topic():
    result = PolicyLookup().run({"topic": "expense.unknown"})
    assert result.category is ResultCategory.INVALID_INPUT


def test_permission_check_allowed():
    result = PermissionCheck().run(
        {"actor": "carol@contoso.com", "permission": "expense.approve"},
    )
    assert result.category is ResultCategory.OK
    assert result.output is not None
    assert result.output.allowed is True  # type: ignore[attr-defined]


def test_permission_check_denied():
    result = PermissionCheck().run(
        {"actor": "alice@contoso.com", "permission": "expense.approve"},
    )
    assert result.category is ResultCategory.OK
    assert result.output is not None
    assert result.output.allowed is False  # type: ignore[attr-defined]


def test_permission_check_unknown_actor_refused():
    result = PermissionCheck().run(
        {"actor": "stranger@unknown.example", "permission": "expense.read"},
    )
    assert result.category is ResultCategory.REFUSED


def test_document_search_ranks_matches():
    result = DocumentSearch().run({"query": "travel policy expense", "limit": 3})
    assert result.category is ResultCategory.OK
    assert result.output is not None
    titles = [hit.title for hit in result.output.hits]  # type: ignore[attr-defined]
    assert "FY26 Travel Policy" in titles


def test_document_search_validates_query_length():
    result = DocumentSearch().run({"query": "x", "limit": 1})
    assert result.category is ResultCategory.INVALID_INPUT


def test_ticket_open_creates_ticket():
    result = TicketOpen().run(
        {
            "actor": "bob@contoso.com",
            "category": "expense",
            "title": "Reimbursement for client trip",
            "body": "USD 1800 trip to a new client; need director approval per policy.",
        },
    )
    assert result.category is ResultCategory.OK
    assert result.output is not None
    assert result.output.ticket_id.startswith("TCK-")  # type: ignore[attr-defined]


def test_ticket_open_rejects_unknown_category():
    result = TicketOpen().run(
        {
            "actor": "bob@contoso.com",
            "category": "magic",
            "title": "Reimbursement for client trip",
            "body": "USD 1800 trip to a new client; need director approval per policy.",
        },
    )
    assert result.category is ResultCategory.INVALID_INPUT


def test_ticket_open_refuses_blocked_actor():
    result = TicketOpen().run(
        {
            "actor": "test_refused_actor@contoso.com",
            "category": "expense",
            "title": "Reimbursement for client trip",
            "body": "USD 1800 trip to a new client; need director approval per policy.",
        },
    )
    assert result.category is ResultCategory.REFUSED


def test_evidence_log_appends_row():
    evidence_reset()
    result = EvidenceLog().run(
        {
            "actor": "bob@contoso.com",
            "action": "ticket_open",
            "decision": "executed",
            "correlation_id": "abc-123",
            "notes": "TCK-DEADBEEF",
        },
    )
    assert result.category is ResultCategory.OK
    rows = evidence_dump()
    assert len(rows) == 1
    assert rows[0]["decision"] == "executed"


def test_justification_draft_quotes_topic():
    result = JustificationDraft().run(
        {
            "actor": "bob@contoso.com",
            "action": "ticket_open",
            "policy_topic": "expense.travel",
            "rationale": "Director approval requested for travel above USD 1500",
        },
    )
    assert result.category is ResultCategory.OK
    assert result.output is not None
    assert "expense.travel" in result.output.text  # type: ignore[attr-defined]


@pytest.fixture(autouse=True)
def _reset_evidence_log():
    evidence_reset()
    yield
    evidence_reset()
