from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class AssistantResponse:
    next_step: str
    confidence: float
    needs_confirmation: bool



def normalize_assistant_output(raw: str) -> AssistantResponse:
    """Try to parse structured output; fallback to robust plain-text response."""
    cleaned = (raw or "").strip()
    if not cleaned:
        return AssistantResponse(
            next_step="Şu an yanıt üretemedim, tekrar dener misin?",
            confidence=0.1,
            needs_confirmation=True,
        )

    try:
        payload = json.loads(cleaned)
        next_step = str(payload.get("next_step", "")).strip()
        confidence = float(payload.get("confidence", 0.5))
        needs_confirmation = bool(payload.get("needs_confirmation", confidence < 0.65))
        if not next_step:
            raise ValueError("next_step boş")
        return AssistantResponse(
            next_step=next_step,
            confidence=max(0.0, min(1.0, confidence)),
            needs_confirmation=needs_confirmation,
        )
    except Exception:
        return AssistantResponse(
            next_step=cleaned,
            confidence=0.55,
            needs_confirmation=True,
        )
