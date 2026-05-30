from pathlib import Path

from nexu.capsule import create_capsule
from nexu.init_project import init_project
from nexu.mcp_server import MCP_TOOLS, call_tool, handle_mcp_message
from nexu.orchestrate import build_capsule_orchestration


def _make_project(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        '# @intract.v1 scope:function intent:preview:item priority:1 domain:demo input:item output:evolved_capsule,promotion_plan,evidence_map effect:read forbid:write,secret_leak validate:output_presence,no_forbidden_effect meaning:"demo"\n'
        'def preview_item(item):\n'
        '    evidence_map = {"item": item}\n'
        '    return {"evolved_capsule": item, "promotion_plan": [], "evidence_map": evidence_map}\n',
        encoding="utf-8",
    )


def test_orchestration_offline(tmp_path: Path):
    _make_project(tmp_path)
    init_project(tmp_path)
    create_capsule(tmp_path, "demo", include=["src/**"], routes=["/demo"], endpoints=["GET:/api/demo"])

    result = build_capsule_orchestration(tmp_path, "demo", steps=3, goal="orchestrate demo")

    assert Path(result["yaml"]).exists()
    assert Path(result["prompt"]).exists()
    assert result["mode"] == "offline_deterministic"
    assert result["steps"] == 3


def test_mcp_tool_dispatch_and_protocol(tmp_path: Path):
    _make_project(tmp_path)
    init_project(tmp_path)
    assert any(tool["name"] == "nexu_capsule_orchestrate" for tool in MCP_TOOLS)

    created = call_tool(
        tmp_path,
        "nexu_capsule_create",
        {"name": "demo", "include": ["src/**"], "routes": ["/demo"], "endpoints": ["GET:/api/demo"]},
    )
    assert created["name"] == "demo"

    response = handle_mcp_message(
        tmp_path,
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
    )
    assert response is not None
    assert response["result"]["tools"]

    called = handle_mcp_message(
        tmp_path,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "nexu_capsule_orchestrate", "arguments": {"name": "demo", "steps": 2}},
        },
    )
    assert called is not None
    assert "content" in called["result"]
