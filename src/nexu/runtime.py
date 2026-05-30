from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import yaml

from .blueprint import build_blueprint
from .capsule import load_capsule
from .intract import read_manifest_contracts
from .journal import append_journal
from .models import utc_now, write_yaml
from .paths import capsule_dir


def _read_fixture(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"binary": path.name, "size": path.stat().st_size}
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return text


def _collect_fixtures(base: Path) -> dict[str, Any]:
    fixtures: dict[str, Any] = {}
    fixture_dir = base / "fixtures"
    if not fixture_dir.exists():
        return fixtures
    for path in sorted(item for item in fixture_dir.rglob("*") if item.is_file()):
        fixtures[path.relative_to(fixture_dir).as_posix()] = _read_fixture(path)
    return fixtures


def _html_page(name: str, data: dict[str, Any]) -> str:
    payload = html.escape(json.dumps(data, ensure_ascii=False, indent=2))
    blueprint = data.get("blueprint", {})
    screens = blueprint.get("ui", {}).get("screens", [])
    endpoints = blueprint.get("api", {}).get("endpoints", [])
    contracts = data.get("contracts", [])
    iterations = data.get("iterations", [])

    screen_cards = "".join(
        f"<li><strong>{html.escape(str(screen.get('route', '')))}</strong> — {html.escape(str(screen.get('layout', '')))}</li>"
        for screen in screens
    ) or "<li>No UI screens declared.</li>"
    endpoint_cards = "".join(
        f"<li><strong>{html.escape(str(endpoint.get('method', 'GET')))}</strong> {html.escape(str(endpoint.get('path', '')))}</li>"
        for endpoint in endpoints
    ) or "<li>No API endpoints declared.</li>"
    contract_cards = "".join(
        f"<li><strong>{html.escape(str(contract.get('intent', '')))}</strong> <code>forbid={html.escape(str(contract.get('forbid', [])))}</code></li>"
        for contract in contracts
    ) or "<li>No contracts loaded.</li>"
    timeline = "".join(f"<li>{html.escape(str(item))}</li>" for item in iterations) or "<li>S0 baseline only.</li>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Vico Capsule Runtime — {html.escape(name)}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; background: #f6f7f9; color: #16181d; }}
    header {{ background: #16181d; color: white; padding: 24px 32px; }}
    main {{ padding: 24px 32px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
    section {{ background: white; border: 1px solid #e2e5ea; border-radius: 14px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,.04); }}
    .wide {{ grid-column: 1 / -1; }}
    code, pre {{ background: #f0f2f5; border-radius: 8px; }}
    pre {{ padding: 16px; overflow: auto; max-height: 420px; }}
    .badge {{ display: inline-block; background: #eef2ff; padding: 4px 8px; border-radius: 999px; margin-right: 6px; }}
  </style>
</head>
<body>
  <header>
    <h1>Vico Capsule Runtime</h1>
    <p><span class="badge">{html.escape(name)}</span><span class="badge">static preview</span><span class="badge">contract-bound sandbox</span></p>
  </header>
  <main>
    <section>
      <h2>UI screens</h2>
      <ul>{screen_cards}</ul>
    </section>
    <section>
      <h2>API endpoints</h2>
      <ul>{endpoint_cards}</ul>
    </section>
    <section>
      <h2>Intent contracts</h2>
      <ul>{contract_cards}</ul>
    </section>
    <section>
      <h2>Iteration timeline</h2>
      <ul>{timeline}</ul>
    </section>
    <section class="wide">
      <h2>Runtime data</h2>
      <pre>{payload}</pre>
    </section>
  </main>
</body>
</html>
"""


def build_capsule_runtime(root: Path, name: str) -> dict[str, Any]:
    capsule = load_capsule(root, name)
    base = capsule_dir(root, name)
    blueprint = build_blueprint(root, name)
    contracts = read_manifest_contracts(base / capsule.contracts_manifest)
    data = {
        "version": "vico.runtime.v1",
        "capsule": name,
        "created_at": utc_now(),
        "blueprint": blueprint,
        "contracts": [contract.__dict__ for contract in contracts],
        "fixtures": _collect_fixtures(base),
        "iterations": capsule.iterations or ["S0"],
    }
    runtime_dir = base / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    (runtime_dir / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (runtime_dir / "index.html").write_text(_html_page(name, data), encoding="utf-8")
    write_yaml(runtime_dir / "runtime.yaml", {"index": "index.html", "data": "data.json", "created_at": data["created_at"]})
    append_journal(root, name, "runtime.built", "Built static capsule runtime.", data={"path": str(runtime_dir / "index.html")})
    return {"index": str(runtime_dir / "index.html"), "data": str(runtime_dir / "data.json"), "created_at": data["created_at"]}
