from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule, save_capsule
from .models import utc_now, write_yaml
from .paths import capsule_dir


def iterate_capsule(root: Path, name: str, *, steps: int, goal: str) -> list[str]:
    capsule = load_capsule(root, name)
    created: list[str] = []
    base = capsule_dir(root, name)
    existing_numbers = [
        int(item[1:])
        for item in capsule.iterations
        if item.startswith("S") and item[1:].isdigit()
    ]
    start = max(existing_numbers or [0]) + 1
    for number in range(start, start + steps):
        state_id = f"S{number}"
        state_dir = base / "iterations" / state_id
        state_dir.mkdir(parents=True, exist_ok=True)
        write_yaml(
            state_dir / "state.yaml",
            {
                "state": state_id,
                "created_at": utc_now(),
                "goal": goal,
                "status": "planned",
                "intent_contract": f"capsule.{name}.main",
                "notes": [
                    "This is a planned capsule iteration.",
                    "Attach LLM or human changes inside the capsule before verification.",
                ],
            },
        )
        prompt = f"""# Vico capsule iteration {state_id}\n\nCapsule: {name}\nGoal: {goal}\n\nRules:\n- Work only inside this capsule.\n- Preserve Intract contracts unless explicitly updated.\n- Do not mutate the source project.\n- After changes, run `vico capsule verify {name}`.\n"""
        (state_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        if state_id not in capsule.iterations:
            capsule.iterations.append(state_id)
        created.append(state_id)
    save_capsule(root, capsule)
    return created
