"""Versioned data models for benchmark cases and results."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Base model that rejects misspelled or undocumented fields."""

    model_config = ConfigDict(extra="forbid")


class Category(StrEnum):
    PROMPT_INJECTION = "prompt_injection"
    SENSITIVE_DATA = "sensitive_data"
    TOOL_AUTHORIZATION = "tool_authorization"
    FINANCIAL_REGULATORY_FACTUALITY = "financial_regulatory_factuality"
    HUMAN_ESCALATION = "human_escalation"
    CONFIDENCE_CITATION = "confidence_citation"


class Mode(StrEnum):
    CHAT = "chat"
    RAG = "rag"
    AGENT = "agent"


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Outcome(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NEEDS_REVIEW = "needs_review"
    ERROR = "error"
    NOT_APPLICABLE = "not_applicable"


class SourceDocument(StrictModel):
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    content: str


class ToolSpec(StrictModel):
    name: str = Field(min_length=1)
    description: str = ""


class Setup(StrictModel):
    system_prompt: str
    context: list[SourceDocument] = Field(default_factory=list)
    tools: list[ToolSpec] = Field(default_factory=list)


class Message(StrictModel):
    role: str = Field(pattern=r"^(system|user|assistant|tool)$")
    content: str


class ExpectedBehavior(StrictModel):
    required_behaviors: list[str] = Field(default_factory=list)
    forbidden_behaviors: list[str] = Field(default_factory=list)
    should_escalate: bool = False
    allowed_tools: list[str] = Field(default_factory=list)
    required_source_ids: list[str] = Field(default_factory=list)


class CheckSpec(StrictModel):
    type: str = Field(min_length=1)
    value: str | None = None
    values: list[str] = Field(default_factory=list)
    critical: bool = False
    case_sensitive: bool = True


class RubricDimension(StrictModel):
    name: str = Field(min_length=1)
    weight: float = Field(default=1.0, gt=0)
    criteria: str = Field(min_length=1)


class Rubric(StrictModel):
    dimensions: list[RubricDimension] = Field(default_factory=list)


class Provenance(StrictModel):
    source_type: str = Field(min_length=1)
    source_urls: list[str] = Field(default_factory=list)
    license: str = Field(min_length=1)
    author: str = Field(min_length=1)
    review_status: str = Field(pattern=r"^(draft|reviewed|approved)$")
    last_reviewed_at: str | None = None


class TestCase(StrictModel):
    id: str = Field(pattern=r"^[A-Z]{2}-[A-Z]{2}-\d{3}$")
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    title: str = Field(min_length=1)
    language: str = Field(pattern=r"^[a-z]{2}$")
    category: Category
    mode: Mode
    severity: Severity
    tags: list[str] = Field(default_factory=list)
    required_capabilities: list[str] = Field(default_factory=list)
    setup: Setup
    messages: list[Message] = Field(min_length=1)
    expected: ExpectedBehavior
    checks: list[CheckSpec] = Field(default_factory=list)
    rubric: Rubric = Field(default_factory=Rubric)
    provenance: Provenance


class ToolCall(StrictModel):
    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class ModelResponse(StrictModel):
    text: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CheckResult(StrictModel):
    check_type: str
    passed: bool | None
    critical: bool
    reason: str


class CaseResult(StrictModel):
    case_id: str
    category: Category
    severity: Severity
    outcome: Outcome
    response: ModelResponse | None = None
    checks: list[CheckResult] = Field(default_factory=list)
    latency_ms: float | None = None
    error: str | None = None
