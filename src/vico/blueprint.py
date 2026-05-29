from __future__ import annotations

from pathlib import Path

from .capsule import load_capsule
from .intract import read_manifest_contracts
from .models import utc_now, write_yaml
from .paths import capsule_dir


def build_blueprint(root: Path, name: str) -> dict:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    contracts = read_manifest_contracts(base / capsule.contracts_manifest)
    routes = capsule.selection.routes
    endpoints = capsule.selection.endpoints

    screens = []
    for route in routes or [f"/capsules/{name}"]:
        screens.append(
            {
                "route": route,
                "layout": "capsule_preview",
                "sections": [
                    {"id": "intent_summary", "type": "summary"},
                    {"id": "input_fixtures", "type": "data_panel"},
                    {"id": "preview", "type": "mock_surface"},
                    {"id": "evidence", "type": "verification_panel"},
                ],
            }
        )

    api = []
    for endpoint in endpoints:
        method, _, path = endpoint.partition(":")
        api.append(
            {
                "method": method or "GET",
                "path": path or endpoint,
                "kind": "mock_endpoint",
                "response": {"status": "ok", "source": "capsule_fixture"},
            }
        )

    blueprint = {
        "version": "vico.blueprint.v1",
        "capsule": name,
        "created_at": utc_now(),
        "type": capsule.type,
        "domain": capsule.selection.domain,
        "contracts": [
            {
                "id": contract.contract_id,
                "intent": contract.intent,
                "input": contract.input,
                "output": contract.output,
                "effect": contract.effect,
                "forbid": contract.forbid,
            }
            for contract in contracts
        ],
        "ui": {"screens": screens},
        "api": {"endpoints": api},
        "tests": {
            "suggested": [
                "contract_outputs_are_present",
                "forbidden_effects_are_absent",
                "capsule_promotion_plan_is_reviewable",
            ]
        },
    }
    write_yaml(base / "blueprints" / "blueprint.yaml", blueprint)
    return blueprint
