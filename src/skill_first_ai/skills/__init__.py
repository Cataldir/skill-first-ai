"""Concrete reusable skills.

Each skill in this package is the same shape: a typed input, a typed
output, a manifest, and an ``_execute`` method that raises typed errors.

The set was chosen to match the provocation from the talk: before
spinning up an "agente financeiro", the question is which capabilities
should already exist. The answer is in this folder.
"""

from skill_first_ai.skills.document_search import DocumentSearch
from skill_first_ai.skills.evidence_log import EvidenceLog
from skill_first_ai.skills.justification import JustificationDraft
from skill_first_ai.skills.permission_check import PermissionCheck
from skill_first_ai.skills.policy_lookup import PolicyLookup
from skill_first_ai.skills.ticket_open import TicketOpen

__all__ = [
    "DocumentSearch",
    "EvidenceLog",
    "JustificationDraft",
    "PermissionCheck",
    "PolicyLookup",
    "TicketOpen",
]
