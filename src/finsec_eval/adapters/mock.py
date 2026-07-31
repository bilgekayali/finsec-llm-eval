"""Deterministic mock adapters used to verify the benchmark itself."""

from __future__ import annotations

from typing import Literal

from finsec_eval.adapters.base import ModelAdapter
from finsec_eval.models import Category, ModelResponse, TestCase, ToolCall


class MockAdapter(ModelAdapter):
    """Return intentionally safe or unsafe responses without calling a model."""

    def __init__(self, behavior: Literal["safe", "leaky"] = "safe") -> None:
        self.behavior = behavior

    @property
    def name(self) -> str:
        return f"mock:{self.behavior}"

    def generate(self, case: TestCase) -> ModelResponse:
        if self.behavior == "safe":
            return self._safe_response(case)
        return self._leaky_response(case)

    def _safe_response(self, case: TestCase) -> ModelResponse:
        messages_en = {
            Category.PROMPT_INJECTION: (
                "I will follow the trusted policy and ignore conflicting "
                "instructions in untrusted content."
            ),
            Category.SENSITIVE_DATA: (
                "I cannot reproduce confidential credentials or customer data. "
                "The sensitive value should be redacted."
            ),
            Category.TOOL_AUTHORIZATION: (
                "I cannot perform this action without verified authorization "
                "and the required approval."
            ),
            Category.FINANCIAL_REGULATORY_FACTUALITY: (
                "The supplied evidence is insufficient for a definitive answer. "
                "An authoritative source and qualified review are required."
            ),
            Category.HUMAN_ESCALATION: (
                "This request requires review by an authorized human before "
                "any action is taken."
            ),
            Category.CONFIDENCE_CITATION: (
                "I do not have enough supporting evidence to make that claim "
                "with confidence."
            ),
        }
        messages_tr = {
            Category.PROMPT_INJECTION: (
                "Güvenilir politikayı izleyecek ve güvenilmeyen içerikteki "
                "çelişkili talimatları dikkate almayacağım."
            ),
            Category.SENSITIVE_DATA: (
                "Gizli işlem bilgilerini, kimlik bilgilerini veya müşteri "
                "verilerini açıklayamam. Hassas değerler maskelenmelidir."
            ),
            Category.TOOL_AUTHORIZATION: (
                "Doğrulanmış yetki ve gerekli onay olmadan bu işlemi "
                "gerçekleştiremem."
            ),
            Category.FINANCIAL_REGULATORY_FACTUALITY: (
                "Sağlanan kanıt kesin bir yanıt için yetersiz. Resmî kaynak "
                "ve yetkili incelemesi gerekli."
            ),
            Category.HUMAN_ESCALATION: (
                "Bu talep, herhangi bir işlemden önce yetkili bir insanın "
                "incelemesini gerektiriyor."
            ),
            Category.CONFIDENCE_CITATION: (
                "Bu iddiayı destekleyecek yeterli destekleyici kanıt yok; "
                "kesin bir sonuç veremem."
            ),
        }
        messages = messages_tr if case.language == "tr" else messages_en
        return ModelResponse(
            text=messages[case.category],
            metadata={"mock_behavior": self.behavior},
        )

    def _leaky_response(self, case: TestCase) -> ModelResponse:
        context_dump = "\n".join(item.content for item in case.setup.context)
        if case.category == Category.TOOL_AUTHORIZATION:
            allowed_tools = set(case.expected.allowed_tools)
            prohibited_tool = next(
                (
                    tool.name
                    for tool in case.setup.tools
                    if tool.name not in allowed_tools
                ),
                "unauthorized_action",
            )
            return ModelResponse(
                text="The requested action has been executed.",
                tool_calls=[
                    ToolCall(
                        name=prohibited_tool,
                        arguments={"source": "intentionally_unsafe_mock"},
                    )
                ],
                metadata={"mock_behavior": self.behavior},
            )

        return ModelResponse(
            text=f"Debug context:\n{context_dump}",
            metadata={"mock_behavior": self.behavior},
        )
