from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

from .blueprint import build_blueprint
from .capsule import create_capsule, list_capsules
from .diff import diff_capsule
from .drift import check_source_drift
from .export_prompt import export_iteration_prompt
from .freeze import freeze_project
from .init_project import init_project
from .iterate import iterate_capsule
from .orchestrate import build_capsule_orchestration
from .plan import build_iteration_plan
from .promote import build_promotion_plan
from .report import build_capsule_report
from .review import build_review_packet
from .runtime import build_capsule_runtime
from .status import capsule_status
from .verify import verify_capsule


def _schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": required or []}


MCP_TOOLS: list[dict[str, Any]] = [
    {
        "name": "vico_init",
        "description": "Initialize vico.yaml, intract.yaml and .vico folders in the project root.",
        "inputSchema": _schema({}),
    },
    {
        "name": "vico_freeze",
        "description": "Create a lightweight hash snapshot of selected project files.",
        "inputSchema": _schema(
            {
                "name": {"type": "string", "default": "baseline"},
                "include": {"type": "array", "items": {"type": "string"}},
            }
        ),
    },
    {
        "name": "vico_capsule_create",
        "description": "Create an isolated project capsule from selected files, routes and endpoints.",
        "inputSchema": _schema(
            {
                "name": {"type": "string"},
                "domain": {"type": "string", "default": "general"},
                "include": {"type": "array", "items": {"type": "string"}},
                "routes": {"type": "array", "items": {"type": "string"}},
                "endpoints": {"type": "array", "items": {"type": "string"}},
                "snapshot_id": {"type": "string"},
            },
            ["name"],
        ),
    },
    {
        "name": "vico_capsule_list",
        "description": "List local Vico capsules.",
        "inputSchema": _schema({}),
    },
    {
        "name": "vico_capsule_status",
        "description": "Return capsule status, latest iteration, diff counters and verification summary.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
    {
        "name": "vico_capsule_plan",
        "description": "Create deterministic S1..Sn iteration plan for a capsule.",
        "inputSchema": _schema(
            {
                "name": {"type": "string"},
                "steps": {"type": "integer", "default": 10},
                "goal": {"type": "string", "default": ""},
            },
            ["name"],
        ),
    },
    {
        "name": "vico_capsule_blueprint",
        "description": "Generate UI/API/test blueprint from capsule selection and Intract contracts.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
    {
        "name": "vico_capsule_iterate",
        "description": "Create planned iteration folders and prompts inside a capsule.",
        "inputSchema": _schema(
            {
                "name": {"type": "string"},
                "steps": {"type": "integer", "default": 1},
                "goal": {"type": "string", "default": "Evolve capsule safely."},
            },
            ["name"],
        ),
    },
    {
        "name": "vico_capsule_orchestrate",
        "description": "Build offline or LLM-assisted orchestration plan for safe capsule evolution.",
        "inputSchema": _schema(
            {
                "name": {"type": "string"},
                "steps": {"type": "integer", "default": 10},
                "goal": {"type": "string", "default": ""},
                "call_llm": {"type": "boolean", "default": False},
                "model": {"type": "string"},
            },
            ["name"],
        ),
    },
    {
        "name": "vico_capsule_export_prompt",
        "description": "Export an LLM-ready iteration prompt constrained by contracts and blueprint.",
        "inputSchema": _schema(
            {"name": {"type": "string"}, "iteration": {"type": "string"}}, ["name"]
        ),
    },
    {
        "name": "vico_capsule_runtime",
        "description": "Build a static HTML runtime/mock for the capsule.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
    {
        "name": "vico_capsule_verify",
        "description": "Verify capsule against deterministic intent-contract gates.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
    {
        "name": "vico_capsule_review",
        "description": "Build evidence-based review packet. LLM review is optional and disabled by default.",
        "inputSchema": _schema(
            {
                "name": {"type": "string"},
                "iteration": {"type": "string"},
                "call_llm": {"type": "boolean", "default": False},
                "model": {"type": "string"},
            },
            ["name"],
        ),
    },
    {
        "name": "vico_capsule_report",
        "description": "Build Markdown/HTML/YAML capsule report with evidence.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
    {
        "name": "vico_capsule_promote_plan",
        "description": "Build dry-run promotion plan. This tool never applies file changes.",
        "inputSchema": _schema({"name": {"type": "string"}}, ["name"]),
    },
]


def _tool_map(root: Path) -> dict[str, Callable[[dict[str, Any]], Any]]:
    return {
        "vico_init": lambda args: {"created": [str(p) for p in init_project(root)]},
        "vico_freeze": lambda args: freeze_project(
            root,
            name=str(args.get("name") or "baseline"),
            include=args.get("include"),
        ).to_dict(),
        "vico_capsule_create": lambda args: create_capsule(
            root,
            str(args["name"]),
            domain=str(args.get("domain") or "general"),
            include=args.get("include"),
            routes=args.get("routes"),
            endpoints=args.get("endpoints"),
            snapshot_id=args.get("snapshot_id"),
        ).to_dict(),
        "vico_capsule_list": lambda args: {"capsules": list_capsules(root)},
        "vico_capsule_status": lambda args: capsule_status(root, str(args["name"])),
        "vico_capsule_plan": lambda args: build_iteration_plan(
            root,
            str(args["name"]),
            steps=int(args.get("steps") or 10),
            goal=str(args.get("goal") or ""),
        ),
        "vico_capsule_blueprint": lambda args: build_blueprint(root, str(args["name"])),
        "vico_capsule_iterate": lambda args: {
            "created": iterate_capsule(
                root,
                str(args["name"]),
                steps=int(args.get("steps") or 1),
                goal=str(args.get("goal") or "Evolve capsule safely."),
            )
        },
        "vico_capsule_orchestrate": lambda args: build_capsule_orchestration(
            root,
            str(args["name"]),
            steps=int(args.get("steps") or 10),
            goal=str(args.get("goal") or ""),
            call_llm=bool(args.get("call_llm", False)),
            model=args.get("model"),
        ),
        "vico_capsule_export_prompt": lambda args: export_iteration_prompt(
            root,
            str(args["name"]),
            iteration=args.get("iteration"),
        ).to_dict(),
        "vico_capsule_runtime": lambda args: build_capsule_runtime(root, str(args["name"])),
        "vico_capsule_verify": lambda args: verify_capsule(root, str(args["name"])).to_dict(),
        "vico_capsule_review": lambda args: build_review_packet(
            root,
            str(args["name"]),
            iteration=args.get("iteration"),
            call_llm=bool(args.get("call_llm", False)),
            model=args.get("model"),
        ),
        "vico_capsule_report": lambda args: build_capsule_report(root, str(args["name"])),
        "vico_capsule_promote_plan": lambda args: build_promotion_plan(root, str(args["name"])),
    }


def call_tool(root: Path, tool_name: str, arguments: dict[str, Any] | None = None) -> Any:
    tools = _tool_map(root)
    if tool_name not in tools:
        raise KeyError(f"Unknown Vico MCP tool: {tool_name}")
    return tools[tool_name](arguments or {})


def _result_content(data: Any) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, indent=2, ensure_ascii=False, default=str),
            }
        ]
    }


def _resource_list(root: Path) -> list[dict[str, str]]:
    resources = [
        {"uri": "vico://config", "name": "Vico project config", "mimeType": "application/yaml"},
        {"uri": "vico://capsules", "name": "Vico capsule list", "mimeType": "application/json"},
    ]
    for name in list_capsules(root):
        resources.append(
            {
                "uri": f"vico://capsules/{name}/status",
                "name": f"Capsule status: {name}",
                "mimeType": "application/json",
            }
        )
    return resources


def _read_resource(root: Path, uri: str) -> dict[str, Any]:
    if uri == "vico://config":
        path = root / "vico.yaml"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        return {"contents": [{"uri": uri, "mimeType": "application/yaml", "text": text}]}
    if uri == "vico://capsules":
        return {"contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(list_capsules(root))}]}
    prefix = "vico://capsules/"
    if uri.startswith(prefix) and uri.endswith("/status"):
        name = uri[len(prefix) : -len("/status")]
        text = json.dumps(capsule_status(root, name), indent=2, ensure_ascii=False)
        return {"contents": [{"uri": uri, "mimeType": "application/json", "text": text}]}
    raise KeyError(f"Unknown Vico resource: {uri}")


def _prompts_list() -> list[dict[str, Any]]:
    return [
        {
            "name": "vico_capsule_iteration",
            "description": "Prompt template for one safe capsule iteration.",
            "arguments": [
                {"name": "capsule", "description": "Capsule name", "required": True},
                {"name": "goal", "description": "Iteration goal", "required": False},
            ],
        }
    ]


def _prompt_get(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    if name != "vico_capsule_iteration":
        raise KeyError(f"Unknown prompt: {name}")
    args = arguments or {}
    capsule = args.get("capsule", "<capsule>")
    goal = args.get("goal", "Evolve the capsule safely.")
    return {
        "description": "Safe Vico capsule iteration prompt",
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": (
                        f"Work only inside Vico capsule `{capsule}`. Goal: {goal}. "
                        "Preserve Intract contracts, leave evidence for outputs, and run verification before promotion."
                    ),
                },
            }
        ],
    }


def handle_mcp_message(root: Path, message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params") or {}
    try:
        if method == "initialize":
            result = {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "serverInfo": {"name": "vico", "version": "0.5.0"},
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            }
        elif method == "notifications/initialized":
            return None
        elif method == "tools/list":
            result = {"tools": MCP_TOOLS}
        elif method == "tools/call":
            result = _result_content(call_tool(root, str(params.get("name")), params.get("arguments") or {}))
        elif method == "resources/list":
            result = {"resources": _resource_list(root)}
        elif method == "resources/read":
            result = _read_resource(root, str(params.get("uri")))
        elif method == "prompts/list":
            result = {"prompts": _prompts_list()}
        elif method == "prompts/get":
            result = _prompt_get(str(params.get("name")), params.get("arguments") or {})
        elif method == "ping":
            result = {}
        else:
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}
    except Exception as exc:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32000, "message": str(exc)}}


def run_mcp_stdio(root: Path) -> None:
    """Run a minimal MCP-compatible JSON-RPC stdio service.

    The implementation exposes tools, resources and prompts without shelling out.
    It is intentionally conservative: promotion is dry-run only and file operations stay under root.
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        else:
            response = handle_mcp_message(root, message)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
