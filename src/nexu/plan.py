from __future__ import annotations

from pathlib import Path
from typing import Any

from .blueprint import build_blueprint
from .capsule import load_capsule
from .intract import read_manifest_contracts
from .journal import append_journal
from .models import utc_now, write_yaml
from .paths import capsule_dir

DEFAULT_STEP_THEMES = [
    ("stabilize_baseline", "Confirm the frozen slice, fixtures and contract boundaries."),
    ("shape_contract", "Make the main intent contract explicit and remove ambiguity."),
    ("mock_data", "Prepare focused fixtures and fake runtime data for fast iterations."),
    ("draft_surface", "Create the first visible UI/API surface for the capsule."),
    ("add_feedback", "Expose confidence, reason, validation messages or response details."),
    ("handle_edges", "Cover empty, invalid, denied and low-confidence states."),
    ("guard_effects", "Separate preview/read-only flows from apply/write flows."),
    ("test_contract", "Add tests or checks that prove declared outputs and forbids."),
    ("polish_flow", "Improve naming, layout, ordering and operator usability."),
    ("promote_ready", "Prepare promotion map, evidence report and final review notes."),
]


def _contract_summary(contracts: list[Any]) -> dict[str, Any]:
    outputs = sorted({item for contract in contracts for item in contract.output})
    forbids = sorted({item for contract in contracts for item in contract.forbid})
    requires = sorted({item for contract in contracts for item in contract.require})
    intents = [contract.intent for contract in contracts if contract.intent]
    return {"intents": intents, "outputs": outputs, "forbid": forbids, "require": requires}


def build_iteration_plan(root: Path, name: str, *, steps: int = 10, goal: str = "") -> dict[str, Any]:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    contracts = read_manifest_contracts(base / capsule.contracts_manifest)
    blueprint = build_blueprint(root, name)
    contract_summary = _contract_summary(contracts)

    planned_steps = []
    for index in range(1, max(1, steps) + 1):
        theme, default_goal = DEFAULT_STEP_THEMES[(index - 1) % len(DEFAULT_STEP_THEMES)]
        state = f"S{index}"
        focus_outputs = contract_summary["outputs"][:3]
        planned_steps.append(
            {
                "state": state,
                "theme": theme,
                "title": theme.replace("_", " ").title(),
                "goal": goal if index == 1 and goal else default_goal,
                "expected_delta": {
                    "ui": "update capsule blueprint or mock surface" if blueprint["ui"]["screens"] else "none",
                    "api": "update mock endpoint or response" if blueprint["api"]["endpoints"] else "none",
                    "data": "update fixtures only when needed",
                    "tests": "add or update evidence for this step",
                },
                "verification_focus": [
                    "no forbidden effects",
                    "outputs have evidence",
                    "capsule diff is reviewable",
                ],
                "outputs_to_prove": focus_outputs,
            }
        )

    plan = {
        "version": "nexu.iteration_plan.v1",
        "capsule": name,
        "created_at": utc_now(),
        "horizon": steps,
        "goal": goal or "Evolve capsule through controlled, contract-bound iterations.",
        "contract_summary": contract_summary,
        "steps": planned_steps,
    }
    plan_dir = base / "plan"
    plan_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(plan_dir / "iteration-plan.yaml", plan)
    append_journal(root, name, "plan.created", f"Created {steps}-step iteration plan.", data={"goal": plan["goal"]})
    return plan
