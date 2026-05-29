# @intract.v1 scope:function intent:preview:menu_icon_normalization priority:1 domain:menu input:menu_items,legacy_icons output:preview_changes,svg_icon_tokens effect:read forbid:write,network validate:input_presence,output_presence,no_forbidden_effect meaning:"show dry-run menu icon migration preview"


def preview_menu_icons(menu_items):
    mapping = {
        "👤": "svg:user",
        "🧪": "svg:test-tube",
        "📊": "svg:chart",
        "⚙️": "svg:settings",
    }
    changes = []
    for item in menu_items:
        icon = item.get("icon")
        suggested = mapping.get(icon)
        if suggested:
            changes.append(
                {
                    "item_id": item["item_id"],
                    "current_icon": icon,
                    "svg_icon_tokens": suggested,
                    "confidence": 0.9,
                }
            )
    return {"preview_changes": changes}
