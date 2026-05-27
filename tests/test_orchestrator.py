"""End-to-end orchestrator test: same six skills, one decision."""

from __future__ import annotations

from skill_first_ai.contracts.skill import ResultCategory
from skill_first_ai.orchestrator.finance_agent import (
    FinanceAgent,
    FinanceRequest,
)
from skill_first_ai.registry.registry import default_registry
from skill_first_ai.skills.evidence_log import evidence_dump, evidence_reset


def test_orchestrator_happy_path_executes_and_logs():
    evidence_reset()
    agent = FinanceAgent(registry=default_registry())
    response = agent.handle(
        FinanceRequest(
            actor="carol@contoso.com",
            intent="travel reimbursement above USD 1500 needs director approval",
            policy_topic="expense.travel",
            required_permission="expense.approve",
            ticket_title="Travel reimbursement for client visit",
            ticket_body="USD 1800 to attend Dengo workshop; director approval per policy.",
        ),
    )
    assert response.decision == "executed"
    assert response.ticket_id and response.ticket_id.startswith("TCK-")
    assert response.justification and "expense.travel" in response.justification
    assert response.refusal_reason is None
    assert len(response.traces) >= 5
    rows = evidence_dump()
    assert len(rows) == 1 and rows[0]["decision"] == "executed"


def test_orchestrator_refuses_when_permission_denied():
    evidence_reset()
    agent = FinanceAgent(registry=default_registry())
    response = agent.handle(
        FinanceRequest(
            actor="alice@contoso.com",  # has submit, not approve
            intent="approve reimbursement above USD 1500",
            policy_topic="expense.travel",
            required_permission="expense.approve",
            ticket_title="Travel reimbursement for client visit",
            ticket_body="USD 1800 to attend Dengo workshop; director approval per policy.",
        ),
    )
    assert response.decision == "refused"
    assert response.ticket_id is None
    assert (
        response.refusal_reason
        and "does not hold the requested permission" in response.refusal_reason
    )


def test_orchestrator_refuses_unknown_actor():
    evidence_reset()
    agent = FinanceAgent(registry=default_registry())
    response = agent.handle(
        FinanceRequest(
            actor="stranger@unknown.example",
            intent="anything",
            policy_topic="expense.travel",
            required_permission="expense.read",
            ticket_title="Travel reimbursement for client visit",
            ticket_body="USD 1800 to attend Dengo workshop; director approval per policy.",
        ),
    )
    assert response.decision == "refused"
    assert response.ticket_id is None
