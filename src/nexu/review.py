from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .blueprint import build_blueprint
from .config import load_config
from .diff import diff_capsule
from .drift import check_source_drift
from .export_prompt import export_iteration_prompt
from .journal import append_journal
from .llm import REVIEW_RESPONSE_SCHEMA, call_litellm_review, offline_review_from_status
from .models import utc_now, write_yaml
from .paths import capsule_dir
from .verify import verify_capsule


def _markdown_review_prompt(packet: dict[str, Any]) -> str:
    return f"""# Vico capsule review request

Capsule: `{packet['capsule']}`
Created at: {packet['created_at']}
Mode: {packet['mode']}

## Task

Review whether this capsule can be promoted back to the source project.
Do not judge by vibes. Use only the evidence below.

Return JSON matching this schema:

```json
{yaml.safe_dump(REVIEW_RESPONSE_SCHEMA, sort_keys=False, allow_unicode=True)}
```

## Verification

```yaml
{yaml.safe_dump(packet['verification'], sort_keys=False, allow_unicode=True)}
```

## Diff

```yaml
{yaml.safe_dump(packet['diff'], sort_keys=False, allow_unicode=True)}
```

## Source drift

```yaml
{yaml.safe_dump(packet['drift'], sort_keys=False, allow_unicode=True)}
```

## Blueprint

```yaml
{yaml.safe_dump(packet['blueprint'], sort_keys=False, allow_unicode=True)}
```

## Deterministic decision

```yaml
{yaml.safe_dump(packet['deterministic_review'], sort_keys=False, allow_unicode=True)}
```
"""


def build_review_packet(
    root: Path,
    name: str,
    *,
    iteration: str | None = None,
    call_llm: bool = False,
    model: str | None = None,
) -> dict[str, Any]:
    config = load_config(root)
    base = capsule_dir(root, name)
    reviews_dir = base / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    verification = verify_capsule(root, name)
    diff = diff_capsule(root, name)
    drift = check_source_drift(root, name)
    blueprint = build_blueprint(root, name)
    prompt_export = export_iteration_prompt(root, name, iteration=iteration)
    deterministic = offline_review_from_status(verification.status, verification.score)

    packet: dict[str, Any] = {
        "version": "vico.review.v1",
        "capsule": name,
        "created_at": utc_now(),
        "mode": "offline" if not call_llm else "llm_requested",
        "config": {
            "project_name": config.project_name,
            "llm_provider": config.llm.provider,
            "llm_model": model or config.llm.model,
            "require_human_approval": config.review.require_human_approval,
        },
        "prompt_export": prompt_export.to_dict(),
        "verification": verification.to_dict(),
        "diff": diff.to_dict(),
        "drift": drift,
        "blueprint": blueprint,
        "review_schema": REVIEW_RESPONSE_SCHEMA,
        "deterministic_review": deterministic,
    }
    prompt = _markdown_review_prompt(packet)
    (reviews_dir / "review-prompt.md").write_text(prompt, encoding="utf-8")

    if call_llm:
        llm_result = call_litellm_review(prompt, config=config.llm, model_override=model)
        packet["llm_review"] = llm_result
    else:
        packet["llm_review"] = None

    write_yaml(reviews_dir / "review.yaml", packet)
    markdown = f"""# Vico review — {name}

Created at: {packet['created_at']}

## Decision

- Deterministic decision: **{deterministic['decision']}**
- Verification status: **{verification.status}**
- Verification score: **{verification.score:.3f}**
- Source drift: **{drift.get('status')}**
- LLM review: **{'enabled' if call_llm else 'not called'}**

## Next action

{deterministic['next_action']}

## Files

- Review YAML: `reviews/review.yaml`
- Review prompt: `reviews/review-prompt.md`
- Iteration prompt: `{Path(prompt_export.path).name}`
"""
    (reviews_dir / "review.md").write_text(markdown, encoding="utf-8")
    append_journal(
        root,
        name,
        "review.built",
        "Built capsule review packet.",
        data={"decision": deterministic["decision"], "call_llm": call_llm},
    )
    return {
        "yaml": str(reviews_dir / "review.yaml"),
        "markdown": str(reviews_dir / "review.md"),
        "prompt": str(reviews_dir / "review-prompt.md"),
        "decision": deterministic["decision"],
        "status": verification.status,
        "score": verification.score,
        "llm_called": call_llm,
    }
