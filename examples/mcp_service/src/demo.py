# @intract.v1 scope:function intent:orchestrate:demo_capsule priority:1 domain:mcp input:user_goal output:evolved_capsule,promotion_plan,evidence_map effect:read forbid:write,secret_leak validate:output_presence,no_forbidden_effect meaning:"demo function for MCP-driven Vico orchestration"


def plan_demo(user_goal: str) -> dict:
    evidence_map = {"goal": user_goal, "mode": "mcp"}
    return {
        "evolved_capsule": user_goal,
        "promotion_plan": [],
        "evidence_map": evidence_map,
    }
