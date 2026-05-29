# Intent contracts

Vico uses Intract-style contracts:

```text
@intract.v1 scope:<scope> intent:<action>:<object> priority:<1-5> domain:<domain> input:<inputs> output:<outputs> effect:<effects> forbid:<effects> require:<subintents> validate:<rules> meaning:"plain explanation"
```

Example:

```python
# @intract.v1 scope:function intent:preview:menu_icon_normalization priority:1 domain:menu input:menu_items,legacy_icons output:preview_changes,svg_icon_tokens effect:read forbid:write,network validate:input_presence,output_presence,no_forbidden_effect meaning:"show dry-run menu icon migration preview"
def preview_menu_icons(items):
    ...
```

Vico treats the contract as an executable specification:

- `input` and `output` define expected evidence,
- `effect` defines allowed side effects,
- `forbid` defines hard constraints,
- `require` links a larger goal to smaller implementation intents.
