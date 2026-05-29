# Vico

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `nexu`
- **version**: `0.2.5`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: nexu;
  version: 0.2.5;
}

dependencies {
  runtime: "pyyaml>=6.0, typer>=0.12.0, rich>=13.0";
  dev: "pytest>=7.0, ruff>=0.4, mypy>=1.8, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="vico"] {

}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=pytest -q;
}

workflow[name="examples"] {
  trigger: manual;
  step-1: run cmd=python examples/run_examples.py;
}

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
}
```

## Workflows

## Dependencies

### Runtime

```text markpact:deps python
pyyaml>=6.0
typer>=0.12.0
rich>=13.0
```

### Development

```text markpact:deps python scope=dev
pytest>=7.0
ruff>=0.4
mypy>=1.8
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Call Graph

*54 nodes · 109 edges · 19 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `verify_capsule` *(in src.vico.verify)* | 45 ⚠ | 2 | 59 | **61** |
| `read_manifest_contracts` *(in src.vico.intract)* | 12 ⚠ | 3 | 32 | **35** |
| `create_capsule` *(in src.vico.capsule)* | 8 | 2 | 22 | **24** |
| `parse_intract_line` *(in src.vico.intract)* | 3 | 1 | 22 | **23** |
| `run_example` *(in examples.run_examples)* | 2 | 1 | 18 | **19** |
| `capsule_diff` *(in src.vico.cli)* | 1 | 0 | 19 | **19** |
| `export_iteration_prompt` *(in src.vico.export_prompt)* | 3 | 2 | 17 | **19** |
| `diff_capsule` *(in src.vico.diff)* | 12 ⚠ | 5 | 14 | **19** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nexu
# generated in 0.03s
# nodes: 54 | edges: 109 | modules: 19
# CC̄=3.5

HUBS[20]:
  src.vico.verify.verify_capsule
    CC=45  in:2  out:59  total:61
  src.vico.intract.read_manifest_contracts
    CC=12  in:3  out:32  total:35
  src.vico.capsule.create_capsule
    CC=8  in:2  out:22  total:24
  src.vico.intract.parse_intract_line
    CC=3  in:1  out:22  total:23
  examples.run_examples.run_example
    CC=2  in:1  out:18  total:19
  src.vico.cli.capsule_diff
    CC=1  in:0  out:19  total:19
  src.vico.export_prompt.export_iteration_prompt
    CC=3  in:2  out:17  total:19
  src.vico.diff.diff_capsule
    CC=12  in:5  out:14  total:19
  src.vico.models.write_yaml
    CC=1  in:14  out:3  total:17
  src.vico.cli.capsule_status_command
    CC=3  in:0  out:17  total:17
  src.vico.iterate.iterate_capsule
    CC=7  in:2  out:14  total:16
  src.vico.cli.capsule_create
    CC=1  in:0  out:15  total:15
  src.vico.paths.project_root
    CC=1  in:12  out:3  total:15
  src.vico.files.collect_files
    CC=8  in:6  out:8  total:14
  src.vico.freeze.freeze_project
    CC=2  in:2  out:12  total:14
  src.vico.blueprint.build_blueprint
    CC=7  in:4  out:8  total:12
  src.vico.drift.check_source_drift
    CC=7  in:2  out:10  total:12
  src.vico.paths.capsule_dir
    CC=1  in:11  out:1  total:12
  src.vico.status.capsule_status
    CC=3  in:1  out:10  total:11
  src.vico.intract._tokenize_contract
    CC=5  in:1  out:10  total:11

MODULES:
  examples.run_examples  [2 funcs]
    main  CC=2  out:1
    run_example  CC=2  out:18
  src.vico.blueprint  [1 funcs]
    build_blueprint  CC=7  out:8
  src.vico.capsule  [4 funcs]
    create_capsule  CC=8  out:22
    list_capsules  CC=4  out:5
    load_capsule  CC=1  out:3
    save_capsule  CC=1  out:3
  src.vico.cli  [12 funcs]
    capsule_blueprint  CC=2  out:10
    capsule_create  CC=1  out:15
    capsule_diff  CC=1  out:19
    capsule_drift  CC=2  out:10
    capsule_export_prompt  CC=1  out:9
    capsule_iterate  CC=1  out:9
    capsule_list  CC=3  out:8
    capsule_promote  CC=2  out:10
    capsule_status_command  CC=3  out:17
    capsule_verify  CC=4  out:10
  src.vico.diff  [1 funcs]
    diff_capsule  CC=12  out:14
  src.vico.drift  [1 funcs]
    check_source_drift  CC=7  out:10
  src.vico.export_prompt  [1 funcs]
    export_iteration_prompt  CC=3  out:17
  src.vico.files  [4 funcs]
    collect_files  CC=8  out:8
    is_text_file  CC=2  out:1
    matches_any  CC=3  out:4
    rel  CC=1  out:2
  src.vico.freeze  [1 funcs]
    freeze_project  CC=2  out:12
  src.vico.git  [1 funcs]
    current_git_sha  CC=4  out:3
  src.vico.hashing  [1 funcs]
    sha256_file  CC=2  out:6
  src.vico.init_project  [1 funcs]
    init_project  CC=3  out:7
  src.vico.intract  [6 funcs]
    _split_csv  CC=4  out:4
    _tokenize_contract  CC=5  out:10
    parse_intract_line  CC=3  out:22
    read_manifest_contracts  CC=12  out:32
    scan_contracts_in_file  CC=3  out:5
    scan_contracts_in_text  CC=3  out:4
  src.vico.iterate  [1 funcs]
    iterate_capsule  CC=7  out:14
  src.vico.models  [4 funcs]
    from_dict  CC=2  out:6
    read_yaml  CC=3  out:4
    utc_now  CC=1  out:2
    write_yaml  CC=1  out:3
  src.vico.paths  [6 funcs]
    capsule_dir  CC=1  out:1
    capsules_dir  CC=1  out:1
    ensure_project_dirs  CC=2  out:7
    project_root  CC=1  out:3
    snapshots_dir  CC=1  out:1
    vico_dir  CC=1  out:0
  src.vico.promote  [1 funcs]
    build_promotion_plan  CC=2  out:6
  src.vico.status  [1 funcs]
    capsule_status  CC=3  out:10
  src.vico.verify  [5 funcs]
    _contains_patterns  CC=3  out:2
    _find_term_evidence  CC=6  out:8
    _scan_capsule_contracts  CC=2  out:4
    _text  CC=2  out:1
    verify_capsule  CC=45  out:59

EDGES:
  examples.run_examples.run_example → src.vico.init_project.init_project
  examples.run_examples.run_example → src.vico.freeze.freeze_project
  examples.run_examples.run_example → src.vico.capsule.create_capsule
  examples.run_examples.run_example → src.vico.blueprint.build_blueprint
  examples.run_examples.run_example → src.vico.iterate.iterate_capsule
  examples.run_examples.run_example → src.vico.export_prompt.export_iteration_prompt
  examples.run_examples.run_example → src.vico.diff.diff_capsule
  examples.run_examples.run_example → src.vico.drift.check_source_drift
  examples.run_examples.main → examples.run_examples.run_example
  src.vico.init_project.init_project → src.vico.paths.ensure_project_dirs
  src.vico.init_project.init_project → src.vico.models.write_yaml
  src.vico.intract.parse_intract_line → src.vico.intract._tokenize_contract
  src.vico.intract.parse_intract_line → src.vico.intract._split_csv
  src.vico.intract.scan_contracts_in_text → src.vico.intract.parse_intract_line
  src.vico.intract.scan_contracts_in_file → src.vico.intract.scan_contracts_in_text
  src.vico.cli.init → src.vico.paths.project_root
  src.vico.cli.init → src.vico.init_project.init_project
  src.vico.cli.freeze → src.vico.paths.project_root
  src.vico.cli.freeze → src.vico.freeze.freeze_project
  src.vico.cli.capsule_create → src.vico.paths.project_root
  src.vico.cli.capsule_create → src.vico.capsule.create_capsule
  src.vico.cli.capsule_create → src.vico.blueprint.build_blueprint
  src.vico.cli.capsule_list → src.vico.paths.project_root
  src.vico.cli.capsule_list → src.vico.capsule.list_capsules
  src.vico.cli.capsule_status_command → src.vico.paths.project_root
  src.vico.cli.capsule_status_command → src.vico.status.capsule_status
  src.vico.cli.capsule_iterate → src.vico.paths.project_root
  src.vico.cli.capsule_iterate → src.vico.iterate.iterate_capsule
  src.vico.cli.capsule_blueprint → src.vico.paths.project_root
  src.vico.cli.capsule_blueprint → src.vico.blueprint.build_blueprint
  src.vico.cli.capsule_export_prompt → src.vico.paths.project_root
  src.vico.cli.capsule_export_prompt → src.vico.export_prompt.export_iteration_prompt
  src.vico.cli.capsule_diff → src.vico.paths.project_root
  src.vico.cli.capsule_diff → src.vico.diff.diff_capsule
  src.vico.cli.capsule_drift → src.vico.paths.project_root
  src.vico.cli.capsule_drift → src.vico.drift.check_source_drift
  src.vico.cli.capsule_verify → src.vico.paths.project_root
  src.vico.cli.capsule_verify → src.vico.verify.verify_capsule
  src.vico.cli.capsule_promote → src.vico.paths.project_root
  src.vico.cli.capsule_promote → src.vico.promote.build_promotion_plan
  src.vico.freeze.freeze_project → src.vico.paths.ensure_project_dirs
  src.vico.freeze.freeze_project → src.vico.models.write_yaml
  src.vico.freeze.freeze_project → src.vico.files.collect_files
  src.vico.freeze.freeze_project → src.vico.git.current_git_sha
  src.vico.freeze.freeze_project → src.vico.paths.snapshots_dir
  src.vico.freeze.freeze_project → src.vico.files.rel
  src.vico.blueprint.build_blueprint → src.vico.capsule.load_capsule
  src.vico.blueprint.build_blueprint → src.vico.paths.capsule_dir
  src.vico.blueprint.build_blueprint → src.vico.intract.read_manifest_contracts
  src.vico.blueprint.build_blueprint → src.vico.models.write_yaml
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nexu
# generated in 0.03s
# nodes: 54 | edges: 109 | modules: 19
# CC̄=3.5

HUBS[20]:
  src.vico.verify.verify_capsule
    CC=45  in:2  out:59  total:61
  src.vico.intract.read_manifest_contracts
    CC=12  in:3  out:32  total:35
  src.vico.capsule.create_capsule
    CC=8  in:2  out:22  total:24
  src.vico.intract.parse_intract_line
    CC=3  in:1  out:22  total:23
  examples.run_examples.run_example
    CC=2  in:1  out:18  total:19
  src.vico.cli.capsule_diff
    CC=1  in:0  out:19  total:19
  src.vico.export_prompt.export_iteration_prompt
    CC=3  in:2  out:17  total:19
  src.vico.diff.diff_capsule
    CC=12  in:5  out:14  total:19
  src.vico.models.write_yaml
    CC=1  in:14  out:3  total:17
  src.vico.cli.capsule_status_command
    CC=3  in:0  out:17  total:17
  src.vico.iterate.iterate_capsule
    CC=7  in:2  out:14  total:16
  src.vico.cli.capsule_create
    CC=1  in:0  out:15  total:15
  src.vico.paths.project_root
    CC=1  in:12  out:3  total:15
  src.vico.files.collect_files
    CC=8  in:6  out:8  total:14
  src.vico.freeze.freeze_project
    CC=2  in:2  out:12  total:14
  src.vico.blueprint.build_blueprint
    CC=7  in:4  out:8  total:12
  src.vico.drift.check_source_drift
    CC=7  in:2  out:10  total:12
  src.vico.paths.capsule_dir
    CC=1  in:11  out:1  total:12
  src.vico.status.capsule_status
    CC=3  in:1  out:10  total:11
  src.vico.intract._tokenize_contract
    CC=5  in:1  out:10  total:11

MODULES:
  examples.run_examples  [2 funcs]
    main  CC=2  out:1
    run_example  CC=2  out:18
  src.vico.blueprint  [1 funcs]
    build_blueprint  CC=7  out:8
  src.vico.capsule  [4 funcs]
    create_capsule  CC=8  out:22
    list_capsules  CC=4  out:5
    load_capsule  CC=1  out:3
    save_capsule  CC=1  out:3
  src.vico.cli  [12 funcs]
    capsule_blueprint  CC=2  out:10
    capsule_create  CC=1  out:15
    capsule_diff  CC=1  out:19
    capsule_drift  CC=2  out:10
    capsule_export_prompt  CC=1  out:9
    capsule_iterate  CC=1  out:9
    capsule_list  CC=3  out:8
    capsule_promote  CC=2  out:10
    capsule_status_command  CC=3  out:17
    capsule_verify  CC=4  out:10
  src.vico.diff  [1 funcs]
    diff_capsule  CC=12  out:14
  src.vico.drift  [1 funcs]
    check_source_drift  CC=7  out:10
  src.vico.export_prompt  [1 funcs]
    export_iteration_prompt  CC=3  out:17
  src.vico.files  [4 funcs]
    collect_files  CC=8  out:8
    is_text_file  CC=2  out:1
    matches_any  CC=3  out:4
    rel  CC=1  out:2
  src.vico.freeze  [1 funcs]
    freeze_project  CC=2  out:12
  src.vico.git  [1 funcs]
    current_git_sha  CC=4  out:3
  src.vico.hashing  [1 funcs]
    sha256_file  CC=2  out:6
  src.vico.init_project  [1 funcs]
    init_project  CC=3  out:7
  src.vico.intract  [6 funcs]
    _split_csv  CC=4  out:4
    _tokenize_contract  CC=5  out:10
    parse_intract_line  CC=3  out:22
    read_manifest_contracts  CC=12  out:32
    scan_contracts_in_file  CC=3  out:5
    scan_contracts_in_text  CC=3  out:4
  src.vico.iterate  [1 funcs]
    iterate_capsule  CC=7  out:14
  src.vico.models  [4 funcs]
    from_dict  CC=2  out:6
    read_yaml  CC=3  out:4
    utc_now  CC=1  out:2
    write_yaml  CC=1  out:3
  src.vico.paths  [6 funcs]
    capsule_dir  CC=1  out:1
    capsules_dir  CC=1  out:1
    ensure_project_dirs  CC=2  out:7
    project_root  CC=1  out:3
    snapshots_dir  CC=1  out:1
    vico_dir  CC=1  out:0
  src.vico.promote  [1 funcs]
    build_promotion_plan  CC=2  out:6
  src.vico.status  [1 funcs]
    capsule_status  CC=3  out:10
  src.vico.verify  [5 funcs]
    _contains_patterns  CC=3  out:2
    _find_term_evidence  CC=6  out:8
    _scan_capsule_contracts  CC=2  out:4
    _text  CC=2  out:1
    verify_capsule  CC=45  out:59

EDGES:
  examples.run_examples.run_example → src.vico.init_project.init_project
  examples.run_examples.run_example → src.vico.freeze.freeze_project
  examples.run_examples.run_example → src.vico.capsule.create_capsule
  examples.run_examples.run_example → src.vico.blueprint.build_blueprint
  examples.run_examples.run_example → src.vico.iterate.iterate_capsule
  examples.run_examples.run_example → src.vico.export_prompt.export_iteration_prompt
  examples.run_examples.run_example → src.vico.diff.diff_capsule
  examples.run_examples.run_example → src.vico.drift.check_source_drift
  examples.run_examples.main → examples.run_examples.run_example
  src.vico.init_project.init_project → src.vico.paths.ensure_project_dirs
  src.vico.init_project.init_project → src.vico.models.write_yaml
  src.vico.intract.parse_intract_line → src.vico.intract._tokenize_contract
  src.vico.intract.parse_intract_line → src.vico.intract._split_csv
  src.vico.intract.scan_contracts_in_text → src.vico.intract.parse_intract_line
  src.vico.intract.scan_contracts_in_file → src.vico.intract.scan_contracts_in_text
  src.vico.cli.init → src.vico.paths.project_root
  src.vico.cli.init → src.vico.init_project.init_project
  src.vico.cli.freeze → src.vico.paths.project_root
  src.vico.cli.freeze → src.vico.freeze.freeze_project
  src.vico.cli.capsule_create → src.vico.paths.project_root
  src.vico.cli.capsule_create → src.vico.capsule.create_capsule
  src.vico.cli.capsule_create → src.vico.blueprint.build_blueprint
  src.vico.cli.capsule_list → src.vico.paths.project_root
  src.vico.cli.capsule_list → src.vico.capsule.list_capsules
  src.vico.cli.capsule_status_command → src.vico.paths.project_root
  src.vico.cli.capsule_status_command → src.vico.status.capsule_status
  src.vico.cli.capsule_iterate → src.vico.paths.project_root
  src.vico.cli.capsule_iterate → src.vico.iterate.iterate_capsule
  src.vico.cli.capsule_blueprint → src.vico.paths.project_root
  src.vico.cli.capsule_blueprint → src.vico.blueprint.build_blueprint
  src.vico.cli.capsule_export_prompt → src.vico.paths.project_root
  src.vico.cli.capsule_export_prompt → src.vico.export_prompt.export_iteration_prompt
  src.vico.cli.capsule_diff → src.vico.paths.project_root
  src.vico.cli.capsule_diff → src.vico.diff.diff_capsule
  src.vico.cli.capsule_drift → src.vico.paths.project_root
  src.vico.cli.capsule_drift → src.vico.drift.check_source_drift
  src.vico.cli.capsule_verify → src.vico.paths.project_root
  src.vico.cli.capsule_verify → src.vico.verify.verify_capsule
  src.vico.cli.capsule_promote → src.vico.paths.project_root
  src.vico.cli.capsule_promote → src.vico.promote.build_promotion_plan
  src.vico.freeze.freeze_project → src.vico.paths.ensure_project_dirs
  src.vico.freeze.freeze_project → src.vico.models.write_yaml
  src.vico.freeze.freeze_project → src.vico.files.collect_files
  src.vico.freeze.freeze_project → src.vico.git.current_git_sha
  src.vico.freeze.freeze_project → src.vico.paths.snapshots_dir
  src.vico.freeze.freeze_project → src.vico.files.rel
  src.vico.blueprint.build_blueprint → src.vico.capsule.load_capsule
  src.vico.blueprint.build_blueprint → src.vico.paths.capsule_dir
  src.vico.blueprint.build_blueprint → src.vico.intract.read_manifest_contracts
  src.vico.blueprint.build_blueprint → src.vico.models.write_yaml
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 30f 2196L | python:24,yaml:2,shell:2,toml:1 | 2026-05-29
# generated in 0.00s
# CC̅=3.5 | critical:1/66 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    verify_capsule CC=45 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[23]:
  [1] Src [main]: main → run_example → init_project → ensure_project_dirs → ...(1 more)
      PURITY: 100% pure
  [2] Src [list_users]: list_users
      PURITY: 100% pure
  [3] Src [preview_menu_icons]: preview_menu_icons
      PURITY: 100% pure
  [4] Src [init]: init → project_root
      PURITY: 100% pure
  [5] Src [freeze]: freeze → project_root
      PURITY: 100% pure
  [6] Src [capsule_create]: capsule_create → project_root
      PURITY: 100% pure
  [7] Src [capsule_list]: capsule_list → project_root
      PURITY: 100% pure
  [8] Src [capsule_status_command]: capsule_status_command → project_root
      PURITY: 100% pure
  [9] Src [capsule_iterate]: capsule_iterate → project_root
      PURITY: 100% pure
  [10] Src [capsule_blueprint]: capsule_blueprint → project_root
      PURITY: 100% pure
  [11] Src [capsule_export_prompt]: capsule_export_prompt → project_root
      PURITY: 100% pure
  [12] Src [capsule_diff]: capsule_diff → project_root
      PURITY: 100% pure
  [13] Src [capsule_drift]: capsule_drift → project_root
      PURITY: 100% pure
  [14] Src [capsule_verify]: capsule_verify → project_root
      PURITY: 100% pure
  [15] Src [capsule_promote]: capsule_promote → project_root
      PURITY: 100% pure
  [16] Src [sha256_text]: sha256_text
      PURITY: 100% pure
  [17] Src [to_dict]: to_dict
      PURITY: 100% pure
  [18] Src [from_dict]: from_dict → utc_now
      PURITY: 100% pure
  [19] Src [to_dict]: to_dict
      PURITY: 100% pure
  [20] Src [from_dict]: from_dict → utc_now
      PURITY: 100% pure
  [21] Src [to_dict]: to_dict
      PURITY: 100% pure
  [22] Src [to_dict]: to_dict
      PURITY: 100% pure
  [23] Src [to_dict]: to_dict
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.6    ←in:0  →out:0
  │ !! verify                     236L  0C    5m  CC=45     ←2
  │ cli                        219L  0C   12m  CC=4      ←0
  │ models                     154L  9C   10m  CC=3      ←11
  │ intract                    125L  1C    6m  CC=12     ←3
  │ capsule                    122L  0C    5m  CC=8      ←10
  │ export_prompt              100L  0C    2m  CC=3      ←2
  │ blueprint                   73L  0C    1m  CC=7      ←3
  │ init_project                62L  0C    1m  CC=3      ←2
  │ files                       51L  0C    4m  CC=8      ←5
  │ iterate                     44L  0C    1m  CC=7      ←2
  │ drift                       36L  0C    1m  CC=7      ←2
  │ status                      35L  0C    1m  CC=3      ←1
  │ paths                       35L  0C    6m  CC=2      ←12
  │ diff                        35L  0C    1m  CC=12     ←5
  │ promote                     31L  0C    1m  CC=2      ←1
  │ freeze                      26L  0C    1m  CC=2      ←2
  │ git                         22L  0C    1m  CC=4      ←2
  │ hashing                     16L  0C    2m  CC=2      ←4
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __main__                     4L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.4    ←in:0  →out:9  !! split
  │ run_examples                64L  0C    2m  CC=2      ←0
  │ menu_icons                  24L  0C    1m  CC=3      ←0
  │ flow                         9L  0C    1m  CC=1      ←0
  │ users                        8L  0C    1m  CC=4      ←0
  │ menu_items.yaml              7L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  512L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              83L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ Makefile                     7L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │

COUPLING:
            examples  src.vico
  examples        ──         9  !! fan-out
  src.vico        ←9        ──  hub
  CYCLES: none
  HUB: src.vico/ (fan-in=9)
  SMELL: examples/ fan-out=9 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 24f 1536L | 2026-05-29

SUMMARY:
  files_scanned: 24
  total_lines:   1536
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       2406
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 61 func | 18f | 2026-05-29
# generated in 0.00s

NEXT[2] (ranked by impact):
  [1] !! SPLIT-FUNC      verify_capsule  CC=45  fan=24
      WHY: CC=45 exceeds 15
      EFFORT: ~1h  IMPACT: 1080

  [2] !! SPLIT           goal.yaml
      WHY: 512L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.6 → ≤2.5
  max-CC:      45 → ≤20
  god-modules: 1 → 0
  high-CC(≥15): 1 → ≤0
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  (first run — no previous data)
```

## Intent

Visual Intent Contract Orchestrator: freeze project slices, evolve capsules, verify intent contracts.
