from __future__ import annotations

import json
import os
from typing import Any

from .config import LLMConfig


REVIEW_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["decision", "summary", "evidence", "risks", "next_action"],
    "properties": {
        "decision": {"type": "string", "enum": ["approve", "needs_revision", "reject"]},
        "summary": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "next_action": {"type": "string"},
    },
}


ORCHESTRATION_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["mode", "goal", "steps", "risk_notes", "verification_strategy"],
    "properties": {
        "mode": {"type": "string"},
        "goal": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "title", "intent", "prompt", "expected_outputs", "verification"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "intent": {"type": "string"},
                    "prompt": {"type": "string"},
                    "expected_outputs": {"type": "array", "items": {"type": "string"}},
                    "verification": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "risk_notes": {"type": "array", "items": {"type": "string"}},
        "verification_strategy": {"type": "array", "items": {"type": "string"}},
    },
}


def _extract_content(response: Any) -> str:
    """Return message content from LiteLLM/OpenAI-compatible responses."""
    try:
        return response["choices"][0]["message"]["content"]
    except Exception:
        # LiteLLM can also return model-like objects depending on version.
        choices = getattr(response, "choices", None)
        if choices:
            message = getattr(choices[0], "message", None)
            content = getattr(message, "content", None)
            if content:
                return str(content)
    raise RuntimeError("LLM response did not contain choices[0].message.content")


def _strip_fences(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text


def call_litellm_json(
    prompt: str,
    *,
    config: LLMConfig,
    model_override: str | None = None,
    system_prompt: str = "Return JSON only.",
) -> dict[str, Any]:
    """Call LiteLLM/OpenRouter and require a JSON object response.

    Network calls are disabled unless `llm.allow_network_calls: true` is set in `vico.yaml`.
    This function is intentionally small so the rest of Vico can run fully offline.
    """
    if not config.allow_network_calls:
        raise RuntimeError(
            "LLM network calls are disabled. Set llm.allow_network_calls: true in vico.yaml "
            "or use offline orchestration."
        )

    api_key = os.getenv(config.api_key_env)
    if not api_key:
        raise RuntimeError(f"Missing API key environment variable: {config.api_key_env}")

    try:
        from litellm import completion  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError("Install optional dependency with `pip install -e .[llm]` to call LiteLLM.") from exc

    model = model_override or config.model
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": config.temperature,
        "timeout": config.timeout,
        "api_key": api_key,
    }
    if config.provider == "openrouter":
        kwargs["api_base"] = config.base_url
    # Keep this best-effort: some providers support JSON mode, some do not.
    kwargs["response_format"] = {"type": "json_object"}

    response = completion(**kwargs)
    content = _strip_fences(_extract_content(response))
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM did not return valid JSON: {content[:500]}") from exc
    if not isinstance(data, dict):
        raise RuntimeError("LLM JSON response must be an object.")
    data.setdefault("mode", "litellm")
    data.setdefault("model", model)
    return data


def offline_review_from_status(status: str, score: float) -> dict[str, Any]:
    if status == "pass":
        decision = "approve"
        next_action = "Human may review the promotion plan and apply the capsule when ready."
    elif status == "partial":
        decision = "needs_revision"
        next_action = "Create a follow-up capsule iteration for missing evidence before promotion."
    else:
        decision = "reject"
        next_action = "Fix failing gates and re-run verification before asking for review again."

    return {
        "mode": "offline_deterministic",
        "decision": decision,
        "summary": f"Verification status is {status} with score {score:.3f}.",
        "evidence": ["Decision derived from deterministic Vico verification gates."],
        "risks": [] if status == "pass" else ["At least one gate is not fully passing."],
        "next_action": next_action,
    }


def call_litellm_review(prompt: str, *, config: LLMConfig, model_override: str | None = None) -> dict[str, Any]:
    data = call_litellm_json(
        prompt,
        config=config,
        model_override=model_override,
        system_prompt="You are a strict reviewer. Return JSON only. Never approve without evidence.",
    )
    data.setdefault("mode", "litellm")
    data.setdefault("model", model_override or config.model)
    return data
