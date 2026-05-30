# Nexu

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
- **version**: `0.5.2`
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
  version: 0.5.2;
}

dependencies {
  runtime: "pyyaml>=6.0, typer>=0.12.0, rich>=13.0";
  dev: "pytest>=7.0, ruff>=0.4, mypy>=1.8, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="nexu"] {

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

*95 nodes · 207 edges · 29 modules · CC̄=3.7*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `verify_capsule` *(in src.nexu.verify)* | 45 ⚠ | 7 | 59 | **66** |
| `_tool_map` *(in src.nexu.mcp_server)* | 10 ⚠ | 1 | 61 | **62** |
| `load_config` *(in src.nexu.config)* | 6 | 2 | 41 | **43** |
| `read_manifest_contracts` *(in src.nexu.intract)* | 12 ⚠ | 6 | 32 | **38** |
| `build_capsule_report` *(in src.nexu.report)* | 1 | 3 | 32 | **35** |
| `build_capsule_orchestration` *(in src.nexu.orchestrate)* | 2 | 3 | 28 | **31** |
| `create_capsule` *(in src.nexu.capsule)* | 8 | 3 | 24 | **27** |
| `build_review_packet` *(in src.nexu.review)* | 5 | 3 | 24 | **27** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nexu
# generated in 0.05s
# nodes: 95 | edges: 207 | modules: 29
# CC̄=3.7

HUBS[20]:
  src.nexu.verify.verify_capsule
    CC=45  in:7  out:59  total:66
  src.nexu.mcp_server._tool_map
    CC=10  in:1  out:61  total:62
  src.nexu.config.load_config
    CC=6  in:2  out:41  total:43
  src.nexu.intract.read_manifest_contracts
    CC=12  in:6  out:32  total:38
  src.nexu.report.build_capsule_report
    CC=1  in:3  out:32  total:35
  src.nexu.orchestrate.build_capsule_orchestration
    CC=2  in:3  out:28  total:31
  src.nexu.capsule.create_capsule
    CC=8  in:3  out:24  total:27
  src.nexu.review.build_review_packet
    CC=5  in:3  out:24  total:27
  examples.run_examples.run_example
    CC=2  in:1  out:26  total:27
  src.nexu.models.write_yaml
    CC=1  in:22  out:3  total:25
  src.nexu.diff.diff_capsule
    CC=12  in:9  out:14  total:23
  src.nexu.intract.parse_intract_line
    CC=3  in:1  out:22  total:23
  src.nexu.orchestrate.offline_orchestration_from_context
    CC=13  in:1  out:22  total:23
  src.nexu.orchestrate._render_orchestration_markdown
    CC=9  in:1  out:22  total:23
  src.nexu.paths.project_root
    CC=1  in:20  out:3  total:23
  src.nexu.export_prompt.export_iteration_prompt
    CC=3  in:4  out:17  total:21
  src.nexu.paths.capsule_dir
    CC=1  in:19  out:1  total:20
  src.nexu.mcp_server.handle_mcp_message
    CC=14  in:1  out:19  total:20
  src.nexu.cli.capsule_diff
    CC=1  in:0  out:19  total:19
  src.nexu.runtime.build_capsule_runtime
    CC=3  in:3  out:16  total:19

MODULES:
  examples.run_examples  [2 funcs]
    main  CC=2  out:1
    run_example  CC=2  out:26
  src.nexu.blueprint  [1 funcs]
    build_blueprint  CC=7  out:8
  src.nexu.bundle  [2 funcs]
    _should_include  CC=5  out:4
    build_capsule_bundle  CC=3  out:15
  src.nexu.capsule  [4 funcs]
    create_capsule  CC=8  out:24
    list_capsules  CC=4  out:5
    load_capsule  CC=1  out:3
    save_capsule  CC=1  out:3
  src.nexu.cli  [20 funcs]
    capsule_blueprint  CC=2  out:10
    capsule_bundle  CC=1  out:10
    capsule_create  CC=1  out:15
    capsule_diff  CC=1  out:19
    capsule_drift  CC=2  out:10
    capsule_export_prompt  CC=1  out:9
    capsule_iterate  CC=1  out:11
    capsule_journal  CC=2  out:17
    capsule_list  CC=3  out:8
    capsule_orchestrate  CC=1  out:16
  src.nexu.config  [1 funcs]
    load_config  CC=6  out:41
  src.nexu.diff  [1 funcs]
    diff_capsule  CC=12  out:14
  src.nexu.drift  [1 funcs]
    check_source_drift  CC=7  out:10
  src.nexu.export_prompt  [1 funcs]
    export_iteration_prompt  CC=3  out:17
  src.nexu.files  [4 funcs]
    collect_files  CC=8  out:8
    is_text_file  CC=2  out:1
    matches_any  CC=3  out:4
    rel  CC=1  out:2
  src.nexu.freeze  [1 funcs]
    freeze_project  CC=2  out:12
  src.nexu.git  [1 funcs]
    current_git_sha  CC=4  out:3
  src.nexu.hashing  [1 funcs]
    sha256_file  CC=2  out:6
  src.nexu.init_project  [1 funcs]
    init_project  CC=3  out:7
  src.nexu.intract  [6 funcs]
    _split_csv  CC=4  out:4
    _tokenize_contract  CC=5  out:10
    parse_intract_line  CC=3  out:22
    read_manifest_contracts  CC=12  out:32
    scan_contracts_in_file  CC=3  out:5
    scan_contracts_in_text  CC=3  out:4
  src.nexu.iterate  [1 funcs]
    iterate_capsule  CC=7  out:14
  src.nexu.journal  [3 funcs]
    append_journal  CC=2  out:6
    journal_path  CC=1  out:1
    read_journal  CC=5  out:6
  src.nexu.llm  [5 funcs]
    _extract_content  CC=4  out:5
    _strip_fences  CC=7  out:9
    call_litellm_json  CC=8  out:13
    call_litellm_review  CC=2  out:3
    offline_review_from_status  CC=4  out:0
  src.nexu.mcp_server  [7 funcs]
    _read_resource  CC=6  out:11
    _resource_list  CC=2  out:2
    _result_content  CC=1  out:1
    _tool_map  CC=10  out:61
    call_tool  CC=3  out:2
    handle_mcp_message  CC=14  out:19
    run_mcp_stdio  CC=6  out:7
  src.nexu.models  [4 funcs]
    from_dict  CC=2  out:6
    read_yaml  CC=3  out:4
    utc_now  CC=1  out:2
    write_yaml  CC=1  out:3
  src.nexu.orchestrate  [6 funcs]
    _contract_dicts  CC=2  out:0
    _render_orchestration_markdown  CC=9  out:22
    build_capsule_orchestration  CC=2  out:28
    build_orchestration_context  CC=2  out:11
    build_orchestration_prompt  CC=1  out:2
    offline_orchestration_from_context  CC=13  out:22
  src.nexu.paths  [6 funcs]
    capsule_dir  CC=1  out:1
    capsules_dir  CC=1  out:1
    ensure_project_dirs  CC=2  out:7
    nexu_dir  CC=1  out:0
    project_root  CC=1  out:3
    snapshots_dir  CC=1  out:1
  src.nexu.plan  [2 funcs]
    _contract_summary  CC=9  out:3
    build_iteration_plan  CC=7  out:15
  src.nexu.promote  [2 funcs]
    _promotion_map  CC=2  out:4
    build_promotion_plan  CC=6  out:16
  src.nexu.report  [1 funcs]
    build_capsule_report  CC=1  out:32
  src.nexu.review  [2 funcs]
    _markdown_review_prompt  CC=1  out:6
    build_review_packet  CC=5  out:24
  src.nexu.runtime  [3 funcs]
    _collect_fixtures  CC=5  out:7
    _read_fixture  CC=5  out:6
    build_capsule_runtime  CC=3  out:16
  src.nexu.status  [1 funcs]
    capsule_status  CC=3  out:10
  src.nexu.verify  [5 funcs]
    _contains_patterns  CC=3  out:2
    _find_term_evidence  CC=6  out:8
    _scan_capsule_contracts  CC=2  out:4
    _text  CC=2  out:1
    verify_capsule  CC=45  out:59

EDGES:
  src.nexu.status.capsule_status → src.nexu.capsule.load_capsule
  src.nexu.status.capsule_status → src.nexu.paths.capsule_dir
  src.nexu.status.capsule_status → src.nexu.diff.diff_capsule
  src.nexu.status.capsule_status → src.nexu.models.read_yaml
  src.nexu.plan.build_iteration_plan → src.nexu.capsule.load_capsule
  src.nexu.plan.build_iteration_plan → src.nexu.paths.capsule_dir
  src.nexu.plan.build_iteration_plan → src.nexu.intract.read_manifest_contracts
  src.nexu.plan.build_iteration_plan → src.nexu.blueprint.build_blueprint
  src.nexu.plan.build_iteration_plan → src.nexu.plan._contract_summary
  src.nexu.plan.build_iteration_plan → src.nexu.models.write_yaml
  src.nexu.plan.build_iteration_plan → src.nexu.journal.append_journal
  src.nexu.review.build_review_packet → src.nexu.config.load_config
  src.nexu.review.build_review_packet → src.nexu.paths.capsule_dir
  src.nexu.review.build_review_packet → src.nexu.verify.verify_capsule
  src.nexu.review.build_review_packet → src.nexu.diff.diff_capsule
  src.nexu.review.build_review_packet → src.nexu.drift.check_source_drift
  src.nexu.review.build_review_packet → src.nexu.blueprint.build_blueprint
  src.nexu.review.build_review_packet → src.nexu.export_prompt.export_iteration_prompt
  src.nexu.review.build_review_packet → src.nexu.llm.offline_review_from_status
  src.nexu.review.build_review_packet → src.nexu.review._markdown_review_prompt
  src.nexu.drift.check_source_drift → src.nexu.capsule.load_capsule
  src.nexu.drift.check_source_drift → src.nexu.models.write_yaml
  src.nexu.drift.check_source_drift → src.nexu.hashing.sha256_file
  src.nexu.drift.check_source_drift → src.nexu.models.utc_now
  src.nexu.drift.check_source_drift → src.nexu.paths.capsule_dir
  src.nexu.files.collect_files → src.nexu.files.rel
  src.nexu.files.collect_files → src.nexu.files.matches_any
  src.nexu.files.collect_files → src.nexu.files.is_text_file
  src.nexu.llm.call_litellm_json → src.nexu.llm._strip_fences
  src.nexu.llm.call_litellm_json → src.nexu.llm._extract_content
  src.nexu.llm.call_litellm_review → src.nexu.llm.call_litellm_json
  src.nexu.paths.snapshots_dir → src.nexu.paths.nexu_dir
  src.nexu.paths.capsules_dir → src.nexu.paths.nexu_dir
  src.nexu.paths.capsule_dir → src.nexu.paths.capsules_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.nexu_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.snapshots_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.capsules_dir
  src.nexu.runtime._collect_fixtures → src.nexu.runtime._read_fixture
  src.nexu.runtime.build_capsule_runtime → src.nexu.capsule.load_capsule
  src.nexu.runtime.build_capsule_runtime → src.nexu.paths.capsule_dir
  src.nexu.runtime.build_capsule_runtime → src.nexu.blueprint.build_blueprint
  src.nexu.runtime.build_capsule_runtime → src.nexu.intract.read_manifest_contracts
  src.nexu.runtime.build_capsule_runtime → src.nexu.models.write_yaml
  src.nexu.runtime.build_capsule_runtime → src.nexu.journal.append_journal
  src.nexu.runtime.build_capsule_runtime → src.nexu.models.utc_now
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.capsule.load_capsule
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.paths.capsule_dir
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.intract.read_manifest_contracts
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.blueprint.build_blueprint
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.diff.diff_capsule
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
# generated in 0.05s
# nodes: 95 | edges: 207 | modules: 29
# CC̄=3.7

HUBS[20]:
  src.nexu.verify.verify_capsule
    CC=45  in:7  out:59  total:66
  src.nexu.mcp_server._tool_map
    CC=10  in:1  out:61  total:62
  src.nexu.config.load_config
    CC=6  in:2  out:41  total:43
  src.nexu.intract.read_manifest_contracts
    CC=12  in:6  out:32  total:38
  src.nexu.report.build_capsule_report
    CC=1  in:3  out:32  total:35
  src.nexu.orchestrate.build_capsule_orchestration
    CC=2  in:3  out:28  total:31
  src.nexu.capsule.create_capsule
    CC=8  in:3  out:24  total:27
  src.nexu.review.build_review_packet
    CC=5  in:3  out:24  total:27
  examples.run_examples.run_example
    CC=2  in:1  out:26  total:27
  src.nexu.models.write_yaml
    CC=1  in:22  out:3  total:25
  src.nexu.diff.diff_capsule
    CC=12  in:9  out:14  total:23
  src.nexu.intract.parse_intract_line
    CC=3  in:1  out:22  total:23
  src.nexu.orchestrate.offline_orchestration_from_context
    CC=13  in:1  out:22  total:23
  src.nexu.orchestrate._render_orchestration_markdown
    CC=9  in:1  out:22  total:23
  src.nexu.paths.project_root
    CC=1  in:20  out:3  total:23
  src.nexu.export_prompt.export_iteration_prompt
    CC=3  in:4  out:17  total:21
  src.nexu.paths.capsule_dir
    CC=1  in:19  out:1  total:20
  src.nexu.mcp_server.handle_mcp_message
    CC=14  in:1  out:19  total:20
  src.nexu.cli.capsule_diff
    CC=1  in:0  out:19  total:19
  src.nexu.runtime.build_capsule_runtime
    CC=3  in:3  out:16  total:19

MODULES:
  examples.run_examples  [2 funcs]
    main  CC=2  out:1
    run_example  CC=2  out:26
  src.nexu.blueprint  [1 funcs]
    build_blueprint  CC=7  out:8
  src.nexu.bundle  [2 funcs]
    _should_include  CC=5  out:4
    build_capsule_bundle  CC=3  out:15
  src.nexu.capsule  [4 funcs]
    create_capsule  CC=8  out:24
    list_capsules  CC=4  out:5
    load_capsule  CC=1  out:3
    save_capsule  CC=1  out:3
  src.nexu.cli  [20 funcs]
    capsule_blueprint  CC=2  out:10
    capsule_bundle  CC=1  out:10
    capsule_create  CC=1  out:15
    capsule_diff  CC=1  out:19
    capsule_drift  CC=2  out:10
    capsule_export_prompt  CC=1  out:9
    capsule_iterate  CC=1  out:11
    capsule_journal  CC=2  out:17
    capsule_list  CC=3  out:8
    capsule_orchestrate  CC=1  out:16
  src.nexu.config  [1 funcs]
    load_config  CC=6  out:41
  src.nexu.diff  [1 funcs]
    diff_capsule  CC=12  out:14
  src.nexu.drift  [1 funcs]
    check_source_drift  CC=7  out:10
  src.nexu.export_prompt  [1 funcs]
    export_iteration_prompt  CC=3  out:17
  src.nexu.files  [4 funcs]
    collect_files  CC=8  out:8
    is_text_file  CC=2  out:1
    matches_any  CC=3  out:4
    rel  CC=1  out:2
  src.nexu.freeze  [1 funcs]
    freeze_project  CC=2  out:12
  src.nexu.git  [1 funcs]
    current_git_sha  CC=4  out:3
  src.nexu.hashing  [1 funcs]
    sha256_file  CC=2  out:6
  src.nexu.init_project  [1 funcs]
    init_project  CC=3  out:7
  src.nexu.intract  [6 funcs]
    _split_csv  CC=4  out:4
    _tokenize_contract  CC=5  out:10
    parse_intract_line  CC=3  out:22
    read_manifest_contracts  CC=12  out:32
    scan_contracts_in_file  CC=3  out:5
    scan_contracts_in_text  CC=3  out:4
  src.nexu.iterate  [1 funcs]
    iterate_capsule  CC=7  out:14
  src.nexu.journal  [3 funcs]
    append_journal  CC=2  out:6
    journal_path  CC=1  out:1
    read_journal  CC=5  out:6
  src.nexu.llm  [5 funcs]
    _extract_content  CC=4  out:5
    _strip_fences  CC=7  out:9
    call_litellm_json  CC=8  out:13
    call_litellm_review  CC=2  out:3
    offline_review_from_status  CC=4  out:0
  src.nexu.mcp_server  [7 funcs]
    _read_resource  CC=6  out:11
    _resource_list  CC=2  out:2
    _result_content  CC=1  out:1
    _tool_map  CC=10  out:61
    call_tool  CC=3  out:2
    handle_mcp_message  CC=14  out:19
    run_mcp_stdio  CC=6  out:7
  src.nexu.models  [4 funcs]
    from_dict  CC=2  out:6
    read_yaml  CC=3  out:4
    utc_now  CC=1  out:2
    write_yaml  CC=1  out:3
  src.nexu.orchestrate  [6 funcs]
    _contract_dicts  CC=2  out:0
    _render_orchestration_markdown  CC=9  out:22
    build_capsule_orchestration  CC=2  out:28
    build_orchestration_context  CC=2  out:11
    build_orchestration_prompt  CC=1  out:2
    offline_orchestration_from_context  CC=13  out:22
  src.nexu.paths  [6 funcs]
    capsule_dir  CC=1  out:1
    capsules_dir  CC=1  out:1
    ensure_project_dirs  CC=2  out:7
    nexu_dir  CC=1  out:0
    project_root  CC=1  out:3
    snapshots_dir  CC=1  out:1
  src.nexu.plan  [2 funcs]
    _contract_summary  CC=9  out:3
    build_iteration_plan  CC=7  out:15
  src.nexu.promote  [2 funcs]
    _promotion_map  CC=2  out:4
    build_promotion_plan  CC=6  out:16
  src.nexu.report  [1 funcs]
    build_capsule_report  CC=1  out:32
  src.nexu.review  [2 funcs]
    _markdown_review_prompt  CC=1  out:6
    build_review_packet  CC=5  out:24
  src.nexu.runtime  [3 funcs]
    _collect_fixtures  CC=5  out:7
    _read_fixture  CC=5  out:6
    build_capsule_runtime  CC=3  out:16
  src.nexu.status  [1 funcs]
    capsule_status  CC=3  out:10
  src.nexu.verify  [5 funcs]
    _contains_patterns  CC=3  out:2
    _find_term_evidence  CC=6  out:8
    _scan_capsule_contracts  CC=2  out:4
    _text  CC=2  out:1
    verify_capsule  CC=45  out:59

EDGES:
  src.nexu.status.capsule_status → src.nexu.capsule.load_capsule
  src.nexu.status.capsule_status → src.nexu.paths.capsule_dir
  src.nexu.status.capsule_status → src.nexu.diff.diff_capsule
  src.nexu.status.capsule_status → src.nexu.models.read_yaml
  src.nexu.plan.build_iteration_plan → src.nexu.capsule.load_capsule
  src.nexu.plan.build_iteration_plan → src.nexu.paths.capsule_dir
  src.nexu.plan.build_iteration_plan → src.nexu.intract.read_manifest_contracts
  src.nexu.plan.build_iteration_plan → src.nexu.blueprint.build_blueprint
  src.nexu.plan.build_iteration_plan → src.nexu.plan._contract_summary
  src.nexu.plan.build_iteration_plan → src.nexu.models.write_yaml
  src.nexu.plan.build_iteration_plan → src.nexu.journal.append_journal
  src.nexu.review.build_review_packet → src.nexu.config.load_config
  src.nexu.review.build_review_packet → src.nexu.paths.capsule_dir
  src.nexu.review.build_review_packet → src.nexu.verify.verify_capsule
  src.nexu.review.build_review_packet → src.nexu.diff.diff_capsule
  src.nexu.review.build_review_packet → src.nexu.drift.check_source_drift
  src.nexu.review.build_review_packet → src.nexu.blueprint.build_blueprint
  src.nexu.review.build_review_packet → src.nexu.export_prompt.export_iteration_prompt
  src.nexu.review.build_review_packet → src.nexu.llm.offline_review_from_status
  src.nexu.review.build_review_packet → src.nexu.review._markdown_review_prompt
  src.nexu.drift.check_source_drift → src.nexu.capsule.load_capsule
  src.nexu.drift.check_source_drift → src.nexu.models.write_yaml
  src.nexu.drift.check_source_drift → src.nexu.hashing.sha256_file
  src.nexu.drift.check_source_drift → src.nexu.models.utc_now
  src.nexu.drift.check_source_drift → src.nexu.paths.capsule_dir
  src.nexu.files.collect_files → src.nexu.files.rel
  src.nexu.files.collect_files → src.nexu.files.matches_any
  src.nexu.files.collect_files → src.nexu.files.is_text_file
  src.nexu.llm.call_litellm_json → src.nexu.llm._strip_fences
  src.nexu.llm.call_litellm_json → src.nexu.llm._extract_content
  src.nexu.llm.call_litellm_review → src.nexu.llm.call_litellm_json
  src.nexu.paths.snapshots_dir → src.nexu.paths.nexu_dir
  src.nexu.paths.capsules_dir → src.nexu.paths.nexu_dir
  src.nexu.paths.capsule_dir → src.nexu.paths.capsules_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.nexu_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.snapshots_dir
  src.nexu.paths.ensure_project_dirs → src.nexu.paths.capsules_dir
  src.nexu.runtime._collect_fixtures → src.nexu.runtime._read_fixture
  src.nexu.runtime.build_capsule_runtime → src.nexu.capsule.load_capsule
  src.nexu.runtime.build_capsule_runtime → src.nexu.paths.capsule_dir
  src.nexu.runtime.build_capsule_runtime → src.nexu.blueprint.build_blueprint
  src.nexu.runtime.build_capsule_runtime → src.nexu.intract.read_manifest_contracts
  src.nexu.runtime.build_capsule_runtime → src.nexu.models.write_yaml
  src.nexu.runtime.build_capsule_runtime → src.nexu.journal.append_journal
  src.nexu.runtime.build_capsule_runtime → src.nexu.models.utc_now
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.capsule.load_capsule
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.paths.capsule_dir
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.intract.read_manifest_contracts
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.blueprint.build_blueprint
  src.nexu.export_prompt.export_iteration_prompt → src.nexu.diff.diff_capsule
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 42f 3842L | python:35,yaml:3,shell:2,toml:1 | 2026-05-30
# generated in 0.01s
# CC̅=3.7 | critical:1/116 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    verify_capsule CC=45 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[32]:
  [1] Src [list_users]: list_users
      PURITY: 100% pure
  [2] Src [preview_menu_icons]: preview_menu_icons
      PURITY: 100% pure
  [3] Src [sha256_text]: sha256_text
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
  [15] Src [capsule_plan]: capsule_plan → project_root
      PURITY: 100% pure
  [16] Src [capsule_runtime]: capsule_runtime → project_root
      PURITY: 100% pure
  [17] Src [capsule_report]: capsule_report → project_root
      PURITY: 100% pure
  [18] Src [capsule_journal]: capsule_journal → project_root
      PURITY: 100% pure
  [19] Src [capsule_orchestrate]: capsule_orchestrate → project_root
      PURITY: 100% pure
  [20] Src [capsule_review]: capsule_review → project_root
      PURITY: 100% pure
  [21] Src [capsule_bundle]: capsule_bundle → project_root
      PURITY: 100% pure
  [22] Src [capsule_promote]: capsule_promote → project_root
      PURITY: 100% pure
  [23] Src [mcp_tools]: mcp_tools
      PURITY: 100% pure
  [24] Src [mcp_serve]: mcp_serve → project_root
      PURITY: 100% pure
  [25] Src [to_dict]: to_dict
      PURITY: 100% pure
  [26] Src [from_dict]: from_dict → utc_now
      PURITY: 100% pure
  [27] Src [to_dict]: to_dict
      PURITY: 100% pure
  [28] Src [from_dict]: from_dict → utc_now
      PURITY: 100% pure
  [29] Src [to_dict]: to_dict
      PURITY: 100% pure
  [30] Src [to_dict]: to_dict
      PURITY: 100% pure
  [31] Src [to_dict]: to_dict
      PURITY: 100% pure
  [32] Src [main]: main → run_example → init_project → ensure_project_dirs → ...(1 more)
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.8    ←in:0  →out:0
  │ cli                        357L  0C   21m  CC=4      ←0
  │ mcp_server                 355L  0C   10m  CC=14     ←1
  │ !! verify                     236L  0C    5m  CC=45     ←7
  │ orchestrate                232L  0C    6m  CC=13     ←3
  │ llm                        165L  0C    5m  CC=8      ←2
  │ review                     157L  0C    2m  CC=5      ←3
  │ models                     154L  9C   10m  CC=3      ←19
  │ runtime                    131L  0C    4m  CC=9      ←3
  │ intract                    125L  1C    6m  CC=12     ←6
  │ capsule                    124L  0C    5m  CC=8      ←14
  │ export_prompt              100L  0C    2m  CC=3      ←4
  │ report                      94L  0C    3m  CC=2      ←3
  │ init_project                86L  0C    1m  CC=3      ←3
  │ plan                        81L  0C    2m  CC=9      ←4
  │ promote                     77L  0C    2m  CC=6      ←2
  │ config                      77L  3C    2m  CC=6      ←2
  │ blueprint                   73L  0C    1m  CC=7      ←8
  │ bundle                      55L  0C    2m  CC=5      ←2
  │ files                       51L  0C    4m  CC=8      ←6
  │ iterate                     44L  0C    1m  CC=7      ←3
  │ journal                     43L  0C    3m  CC=5      ←8
  │ drift                       36L  0C    1m  CC=7      ←5
  │ status                      35L  0C    1m  CC=3      ←3
  │ paths                       35L  0C    6m  CC=2      ←19
  │ diff                        35L  0C    1m  CC=12     ←9
  │ freeze                      26L  0C    1m  CC=2      ←3
  │ git                         22L  0C    1m  CC=4      ←2
  │ hashing                     16L  0C    2m  CC=2      ←4
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __main__                     4L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.2    ←in:0  →out:15  !! split
  │ run_examples                79L  0C    2m  CC=2      ←0
  │ menu_icons                  24L  0C    1m  CC=3      ←0
  │ demo                        10L  0C    1m  CC=1      ←0
  │ flow                         9L  0C    1m  CC=1      ←0
  │ users                        8L  0C    1m  CC=4      ←0
  │ menu_items.yaml              7L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  512L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              84L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ Makefile                     7L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │

COUPLING:
            examples  src.nexu
  examples        ──        15  !! fan-out
  src.nexu       ←15        ──  hub
  CYCLES: none
  HUB: src.nexu/ (fan-in=15)
  SMELL: examples/ fan-out=15 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 35f 3161L | 2026-05-30

SUMMARY:
  files_scanned: 35
  total_lines:   3161
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       2094
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 110 func | 28f | 2026-05-30
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
  CC̄:          3.8 → ≤2.7
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
  prev CC̄=3.6 → now CC̄=3.8
```

## Intent

Visual Intent Contract Orchestrator: freeze project slices, evolve capsules, verify intent contracts.
