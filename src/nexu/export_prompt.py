from __future__ import annotations

from pathlib import Path

import yaml

from .blueprint import build_blueprint
from .capsule import load_capsule
from .diff import diff_capsule
from .intract import read_manifest_contracts
from .models import PromptExport, utc_now, write_yaml
from .paths import capsule_dir


def _latest_iteration(capsule) -> str:
    if capsule.iterations:
        return capsule.iterations[-1]
    return "S0"


def export_iteration_prompt(root: Path, name: str, *, iteration: str | None = None) -> PromptExport:
    capsule = load_capsule(root, name)
    selected_iteration = iteration or _latest_iteration(capsule)
    base = capsule_dir(root, name)
    contracts = read_manifest_contracts(base / capsule.contracts_manifest)
    blueprint = build_blueprint(root, name)
    diff = diff_capsule(root, name)

    contract_block = yaml.safe_dump(
        [
            {
                "id": contract.contract_id,
                "intent": contract.intent,
                "scope": contract.scope,
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
        ],
        sort_keys=False,
        allow_unicode=True,
    )
    blueprint_block = yaml.safe_dump(blueprint, sort_keys=False, allow_unicode=True)
    diff_block = yaml.safe_dump(diff.to_dict(), sort_keys=False, allow_unicode=True)

    prompt = f"""# nexu LLM iteration prompt

Capsule: `{name}`
Iteration: `{selected_iteration}`
Created at: {utc_now()}

## Mission

Evolve only the isolated capsule. Do not mutate the source project directly.
Every change must remain compatible with the Intract intent contracts.

## Hard rules

- Work only under `.nexu/capsules/{name}/src`.
- Preserve or explicitly update `intract.yaml` when intent changes.
- Do not violate `forbid` fields.
- For every declared `output`, add code, fixture, UI, API, or test evidence.
- After changing the capsule, run `nexu capsule verify {name}`.
- If the requested change needs writes, split preview and apply into separate contracts.

## Intract contracts

```yaml
{contract_block}```

## Current blueprint

```yaml
{blueprint_block}```

## Current capsule diff from baseline

```yaml
{diff_block}```

## Expected response from the LLM/agent

1. Summary of changed files.
2. Why the change satisfies the intent.
3. Evidence for each output.
4. Any remaining risks or missing tests.
"""

    prompt_path = base / "prompts" / f"{selected_iteration}.llm.md"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")
    export = PromptExport(capsule=name, iteration=selected_iteration, path=str(prompt_path))
    write_yaml(base / "prompts" / f"{selected_iteration}.llm.yaml", export.to_dict())
    return export
