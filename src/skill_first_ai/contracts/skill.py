"""Skill contract: the boundary every skill must satisfy.

A skill is not a function. It is a small, named, versioned, governed
capability with an explicit input and output contract and a trace that
explains what happened. Foundry agents, MCP servers, HTTP wrappers, and
internal Python callers all consume the same shape.

The contract has four jobs:

1. *Identity* — a stable name and semantic version so callers can pin.
2. *Translation* — Pydantic schemas convert flexible inputs into typed
   domain models before any side effect runs.
3. *Failure* — every result carries a `ResultCategory` so callers do not
   invent retry policy at the moment of failure.
4. *Evidence* — every call leaves a `SkillTrace` with correlation ID,
   skill name, version, latency, and the category that was returned.

Refusing to call something a skill until it satisfies this contract is
how a capability stays reusable across HR, finance, IT, and customer
service agents instead of fragmenting into N copies of itself.
"""

from __future__ import annotations

import abc
from enum import Enum
from time import perf_counter
from typing import Any, ClassVar, Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class ResultCategory(str, Enum):
    """The four states every skill caller has to handle.

    `OK`, `INVALID_INPUT`, `REFUSED`, and `TEMPORARY_FAILURE` are the
    minimum surface needed to write a retry, escalation, or human-review
    policy without asking the model to invent one at runtime.
    """

    OK = "ok"
    INVALID_INPUT = "invalid_input"
    REFUSED = "refused"
    TEMPORARY_FAILURE = "temporary_failure"


class SkillManifest(BaseModel):
    """Everything a registry, an MCP server, or a Foundry agent needs
    to decide whether to expose a skill.

    The manifest is the only thing a governance review reads. If a field
    is missing, the skill is not ready for any other agent to reuse it.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        description="Stable identifier, lower-snake-case, e.g. policy_lookup",
    )
    version: str = Field(
        description="Semantic version. Breaking input or output shape requires major bump.",
    )
    description: str = Field(
        description=(
            "Single sentence telling the agent when to use the skill. "
            "Treated as model-facing copy: every word is read at runtime."
        ),
    )
    owner: str = Field(
        description="The team that maintains and approves changes.",
    )
    tags: tuple[str, ...] = Field(
        default=(),
        description="Free-form tags used by registry filters and MCP catalogs.",
    )
    side_effects: bool = Field(
        description=(
            "True if the skill mutates state outside its own process "
            "(opens tickets, writes records, charges money)."
        ),
    )
    pii: bool = Field(
        description="True if the skill touches personal data. Drives logging and review path.",
    )
    requires_approval: bool = Field(
        default=False,
        description="If True, the orchestrator must collect a human approval before execution.",
    )


class SkillTrace(BaseModel):
    """Boring evidence that explains what the skill did.

    Boring is a compliment. If the trace is interesting, the skill is
    doing two jobs.
    """

    model_config = ConfigDict(frozen=True)

    correlation_id: str
    skill_name: str
    skill_version: str
    latency_ms: float
    category: ResultCategory


class SkillResult(BaseModel, Generic[OutputT]):
    """The single shape every skill returns. No exceptions thrown for
    business-level failures — categorize them so the caller can route."""

    model_config = ConfigDict(frozen=True)

    category: ResultCategory
    output: OutputT | None
    message: str
    trace: SkillTrace


class BaseSkill(abc.ABC, Generic[InputT, OutputT]):
    """Abstract base every concrete skill subclasses.

    Subclasses declare:

    - ``manifest`` — class-level :class:`SkillManifest` instance.
    - ``InputSchema`` — Pydantic model for accepted inputs.
    - ``OutputSchema`` — Pydantic model for the success payload.
    - ``_execute(payload)`` — the actual work, returning ``OutputSchema``
      or raising one of :class:`InvalidInputError`, :class:`SkillRefused`,
      or :class:`TransientSkillError`.

    The public ``run(payload, correlation_id=None)`` method handles
    timing, error classification, and trace assembly.
    """

    manifest: ClassVar[SkillManifest]
    InputSchema: ClassVar[type[BaseModel]]
    OutputSchema: ClassVar[type[BaseModel]]

    def run(
        self,
        payload: dict[str, Any] | BaseModel,
        *,
        correlation_id: str | None = None,
    ) -> SkillResult[Any]:
        """Validate, execute, classify, trace.

        Accepts either a raw dict (so MCP tool calls map cleanly) or a
        pre-validated Pydantic model (so internal Python callers stay
        type-safe). The same path is used by every consumer.
        """
        started = perf_counter()
        correlation = correlation_id or str(uuid4())

        try:
            parsed = self._coerce_input(payload)
        except InvalidInputError as exc:
            return self._envelope(
                category=ResultCategory.INVALID_INPUT,
                output=None,
                message=str(exc),
                correlation=correlation,
                started=started,
            )

        try:
            result_payload = self._execute(parsed)
        except InvalidInputError as exc:
            category, message, output = ResultCategory.INVALID_INPUT, str(exc), None
        except SkillRefused as exc:
            category, message, output = ResultCategory.REFUSED, str(exc), None
        except TransientSkillError as exc:
            category, message, output = ResultCategory.TEMPORARY_FAILURE, str(exc), None
        else:
            category, message, output = ResultCategory.OK, "ok", result_payload

        return self._envelope(
            category=category,
            output=output,
            message=message,
            correlation=correlation,
            started=started,
        )

    @abc.abstractmethod
    def _execute(self, payload: InputT) -> OutputT:
        """Concrete skill behavior. Raise typed errors instead of
        returning ad-hoc dicts."""

    def _coerce_input(self, payload: dict[str, Any] | BaseModel) -> InputT:
        if isinstance(payload, self.InputSchema):
            return payload  # type: ignore[return-value]
        if isinstance(payload, BaseModel):
            payload = payload.model_dump()
        try:
            return self.InputSchema.model_validate(payload)  # type: ignore[return-value]
        except Exception as exc:  # pragma: no cover - delegated to pydantic
            raise InvalidInputError(str(exc)) from exc

    def _envelope(
        self,
        *,
        category: ResultCategory,
        output: BaseModel | None,
        message: str,
        correlation: str,
        started: float,
    ) -> SkillResult[Any]:
        trace = SkillTrace(
            correlation_id=correlation,
            skill_name=self.manifest.name,
            skill_version=self.manifest.version,
            latency_ms=(perf_counter() - started) * 1000,
            category=category,
        )
        return SkillResult[Any](
            category=category,
            output=output,
            message=message,
            trace=trace,
        )


class SkillError(Exception):
    """Base class for skill errors. Never raised directly; subclass it."""


class InvalidInputError(SkillError):
    """Raised when the input fails domain-level validation that
    Pydantic schema could not capture (state checks, lookups)."""


class SkillRefused(SkillError):
    """Raised when the skill refuses the action by policy.

    Refused is *not* a failure. It is the correct outcome. The orchestrator
    must surface it to the user instead of retrying."""


class TransientSkillError(SkillError):
    """Raised when a downstream system is momentarily unavailable.

    Distinct from a refusal: callers may retry with the same correlation
    ID. The trace records both attempts as one logical operation."""
