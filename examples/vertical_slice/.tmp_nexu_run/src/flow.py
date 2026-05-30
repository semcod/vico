# @intract.v1 scope:module intent:evolve:menu_icon_flow priority:1 domain:menu input:menu_items,user_goal output:preview_screen,api_response,evidence_map effect:read forbid:destructive_write,secret_leak require:preview.menu_icons validate:input_presence,output_presence,no_forbidden_effect meaning:"evolve a vertical slice of the menu icon migration flow"


def run_flow(menu_items):
    return {
        "preview_screen": "Menu Icon Preview",
        "api_response": {"preview_changes": menu_items},
        "evidence_map": {"status": "demo"},
    }
