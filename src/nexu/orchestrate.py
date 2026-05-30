from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .blueprint import build_blueprint
from .capsule import load_capsule
from .config import load_config
from .diff import diff_capsule
from .intract import read_manifest_contracts
from .journal import append_journal
from .llm import ORCHESTRATION_RESPONSE_SCHEMA, call_litellm_json
from .models import utc_now, write_yaml
from .paths import capsule_dir
from .plan import build_iteration_plan
from .verify import verify_capsule


def _contract_dicts(contracts: list[Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": contract.contract_id,
            "scope": contract.scope,
            "intent": contract.intent,
            "priority": contract.priority,
            "domain": contract.domain,
            "input": contract.input,
            "output": contract.output,
            "effect": contract.effect,
            "forbid": contract.forbid,
            "require": contract.require,
            "validate": contract.validate,
            "meaning": contract.meaning,
        }
        for contract in contracts
    ]


def build_orchestration_context(root: Path, name: str, *, steps: int = 10, goal: str = "") -> dict[str, Any]:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    contracts = read_manifest_contracts(base / capsule.contracts_manifest)
    plan = build_iteration_plan(root, name, steps=steps, goal=goal)
    blueprint = build_blueprint(root, name)
    verification = verify_capsule(root, name)
    diff = diff_capsule(root, name)
    return {
        "version": "nexu.orchestration_context.v1",
        "capsule": capsule.to_dict(),
        "goal": goal or plan["goal"],
        "steps": steps,
        "contracts": _contract_dicts(contracts),
        "blueprint": blueprint,
        "iteration_plan": plan,
        "verification": verification.to_dict(),
        "diff": diff.to_dict(),
    }


def build_orchestration_prompt(context: dict[str, Any]) -> str:
    schema_block = yaml.safe_dump(ORCHESTRATION_RESPONSE_SCHEMA, sort_keys=False, allow_unicode=True)
    context_block = yaml.safe_dump(context, sort_keys=False, allow_unicode=True)
    return f"""# nexu orchestration request

You are planning controlled capsule evolution, not editing the source project directly.
Create a step-by-step orchestration that keeps the LLM inside the capsule and preserves Intract contracts.

Return JSON only, matching this schema:

```yaml
{schema_block}```

Rules:

- Every step must be small enough for one IDE-agent iteration.
- Every step must mention which intent contract it protects or extends.
- Never ask the agent to mutate the source project directly.
- If write effects are needed, split read-only preview and write/apply into separate steps.
- Include verification instructions for each step.
- Prefer evidence: output fields, fixtures, tests, UI/API blueprint, runtime mock and promotion plan.

Context:

```yaml
{context_block}```
"""


def offline_orchestration_from_context(context: dict[str, Any]) -> dict[str, Any]:
    plan_steps = context.get("iteration_plan", {}).get("steps", []) or []
    contracts = context.get("contracts", []) or []
    primary_intent = contracts[0].get("intent", "evolve:capsule") if contracts else "evolve:capsule"
    outputs = sorted({item for contract in contracts for item in contract.get("output", [])})
    forbids = sorted({item for contract in contracts for item in contract.get("forbid", [])})

    steps = []
    for item in plan_steps:
        state = item.get("state", f"S{len(steps) + 1}")
        title = item.get("title", "Capsule iteration")
        verification = [
            "run nexu capsule verify",
            "check output evidence",
            "check forbidden effects",
        ]
        if forbids:
            verification.append("prove forbids are not violated: " + ", ".join(forbids[:5]))
        if outputs:
            verification.append("prove outputs: " + ", ".join(outputs[:5]))
        steps.append(
            {
                "id": state,
                "title": title,
                "intent": primary_intent,
                "prompt": (
                    f"Work only inside this capsule. Step {state}: {item.get('goal')}. "
                    "Keep changes small, update fixtures/tests when needed, and leave evidence for every output."
                ),
                "expected_outputs": item.get("outputs_to_prove") or outputs[:3] or ["evidence_map"],
                "verification": verification,
            }
        )

    return {
        "version": "nexu.orchestration.v1",
        "mode": "offline_deterministic",
        "capsule": context.get("capsule", {}).get("name", "capsule"),
        "created_at": utc_now(),
        "goal": context.get("goal", "Evolve capsule safely."),
        "steps": steps,
        "risk_notes": [
            "Offline orchestration is conservative and does not infer hidden project behavior.",
            "Use LLM orchestration only as proposal; verify with deterministic gates before promotion.",
        ],
        "verification_strategy": [
            "After every step: nexu capsule verify <name>",
            "Before promotion: nexu capsule review <name>",
            "Promotion remains dry-run until a human reviews evidence and drift.",
        ],
    }


def build_capsule_orchestration(
    root: Path,
    name: str,
    *,
    steps: int = 10,
    goal: str = "",
    call_llm: bool = False,
    model: str | None = None,
) -> dict[str, Any]:
    config = load_config(root)
    base = capsule_dir(root, name)
    out_dir = base / "orchestration"
    out_dir.mkdir(parents=True, exist_ok=True)

    context = build_orchestration_context(root, name, steps=steps, goal=goal)
    prompt = build_orchestration_prompt(context)
    (out_dir / "orchestration-prompt.md").write_text(prompt, encoding="utf-8")
    write_yaml(out_dir / "orchestration-context.yaml", context)

    if call_llm:
        result = call_litellm_json(
            prompt,
            config=config.llm,
            model_override=model,
            system_prompt=(
                "You are a strict software orchestration planner. Return JSON only. "
                "Do not invent access to files outside the provided capsule context."
            ),
        )
        result.setdefault("version", "nexu.orchestration.v1")
        result.setdefault("mode", "llm")
        result.setdefault("capsule", name)
        result.setdefault("created_at", utc_now())
    else:
        result = offline_orchestration_from_context(context)

    write_yaml(out_dir / "orchestration.yaml", result)
    markdown = _render_orchestration_markdown(result)
    (out_dir / "orchestration.md").write_text(markdown, encoding="utf-8")
    append_journal(
        root,
        name,
        "orchestration.built",
        "Built capsule orchestration plan.",
        data={"mode": result.get("mode"), "steps": len(result.get("steps", [])), "call_llm": call_llm},
    )
    return {
        "yaml": str(out_dir / "orchestration.yaml"),
        "markdown": str(out_dir / "orchestration.md"),
        "prompt": str(out_dir / "orchestration-prompt.md"),
        "context": str(out_dir / "orchestration-context.yaml"),
        "mode": result.get("mode"),
        "steps": len(result.get("steps", [])),
    }


def _render_orchestration_markdown(orchestration: dict[str, Any]) -> str:
    lines = [
        f"# nexu orchestration — {orchestration.get('capsule', 'capsule')}",
        "",
        f"Mode: `{orchestration.get('mode')}`",
        f"Goal: {orchestration.get('goal', '')}",
        "",
        "## Steps",
        "",
    ]
    for step in orchestration.get("steps", []) or []:
        lines.extend(
            [
                f"### {step.get('id')} — {step.get('title')}",
                "",
                f"Intent: `{step.get('intent')}`",
                "",
                step.get("prompt", ""),
                "",
                "Expected outputs: " + ", ".join(step.get("expected_outputs", []) or []),
                "Verification: " + ", ".join(step.get("verification", []) or []),
                "",
            ]
        )
    if orchestration.get("risk_notes"):
        lines.extend(["## Risks", ""])
        lines.extend(f"- {item}" for item in orchestration["risk_notes"])
        lines.append("")
    if orchestration.get("verification_strategy"):
        lines.extend(["## Verification strategy", ""])
        lines.extend(f"- {item}" for item in orchestration["verification_strategy"])
        lines.append("")
    return "\n".join(lines)
