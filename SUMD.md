# Nexu

Visual Intent Contract Orchestrator: freeze project slices, evolve capsules, verify intent contracts.

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `nexu`
- **version**: `0.5.2`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(3 analysis files)

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

## Interfaces

### CLI Entry Points

- `nexu`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m nexu
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m nexu --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m nexu --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m nexu --help" 10000
ASSERT_EXIT_CODE 0
```

## Workflows

## Configuration

```yaml
project:
  name: nexu
  version: 0.5.2
  env: local
```

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

## Deployment

```bash markpact:run
pip install nexu

# development install
pip install -e .[dev]
```

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`vico`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.13/site-packages/cryptography/__init__.py:__version__`

## Makefile Targets

- `test`
- `examples`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# nexu | 54f 3681L | python:51,shell:2,less:1 | 2026-05-30
# stats: 129 func | 13 cls | 54 mod | CC̄=3.9 | critical:9 | cycles:0
# alerts[5]: CC verify_capsule=45; CC handle_mcp_message=14; CC offline_orchestration_from_context=13; CC test_plan_runtime_report_and_journal=13; CC test_review_bundle_and_promotion_prechecks=13
# hotspots[5]: run_example fan=23; verify_capsule fan=23; create_capsule fan=20; _tool_map fan=20; build_review_packet fan=19
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[54]:
  app.doql.less,39
  examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/src/app/users.py,9
  examples/backend_service/.tmp_nexu_run/app/users.py,9
  examples/backend_service/app/users.py,9
  examples/frontend_view/.tmp_nexu_run/.nexu/capsules/demo/src/src/menu_icons.py,25
  examples/frontend_view/.tmp_nexu_run/src/menu_icons.py,25
  examples/frontend_view/src/menu_icons.py,25
  examples/mcp_service/.tmp_nexu_run/.nexu/capsules/demo/src/src/demo.py,11
  examples/mcp_service/.tmp_nexu_run/src/demo.py,11
  examples/mcp_service/src/demo.py,11
  examples/run_examples.py,80
  examples/vertical_slice/.tmp_nexu_run/.nexu/capsules/demo/src/src/flow.py,10
  examples/vertical_slice/.tmp_nexu_run/src/flow.py,10
  examples/vertical_slice/src/flow.py,10
  project.sh,50
  src/nexu/__init__.py,6
  src/nexu/__main__.py,5
  src/nexu/blueprint.py,74
  src/nexu/bundle.py,56
  src/nexu/capsule.py,125
  src/nexu/cli.py,358
  src/nexu/config.py,78
  src/nexu/diff.py,36
  src/nexu/drift.py,37
  src/nexu/export_prompt.py,101
  src/nexu/files.py,52
  src/nexu/freeze.py,27
  src/nexu/git.py,23
  src/nexu/hashing.py,17
  src/nexu/init_project.py,87
  src/nexu/intract.py,126
  src/nexu/iterate.py,45
  src/nexu/journal.py,44
  src/nexu/llm.py,166
  src/nexu/mcp_server.py,356
  src/nexu/models.py,155
  src/nexu/orchestrate.py,233
  src/nexu/paths.py,36
  src/nexu/plan.py,82
  src/nexu/promote.py,78
  src/nexu/report.py,95
  src/nexu/review.py,158
  src/nexu/runtime.py,132
  src/nexu/status.py,36
  src/nexu/verify.py,237
  tests/test_capsule_flow.py,26
  tests/test_capsule_next_stage.py,59
  tests/test_capsule_runtime_report.py,51
  tests/test_intract.py,12
  tests/test_models.py,15
  tests/test_nexu.py,12
  tests/test_orchestration_mcp.py,63
  tests/test_review_bundle.py,46
  tree.sh,2
D:
  examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/src/app/users.py:
    e: list_users
    list_users(filters;users)
  examples/backend_service/.tmp_nexu_run/app/users.py:
    e: list_users
    list_users(filters;users)
  examples/backend_service/app/users.py:
    e: list_users
    list_users(filters;users)
  examples/frontend_view/.tmp_nexu_run/.nexu/capsules/demo/src/src/menu_icons.py:
    e: preview_menu_icons
    preview_menu_icons(menu_items)
  examples/frontend_view/.tmp_nexu_run/src/menu_icons.py:
    e: preview_menu_icons
    preview_menu_icons(menu_items)
  examples/frontend_view/src/menu_icons.py:
    e: preview_menu_icons
    preview_menu_icons(menu_items)
  examples/mcp_service/.tmp_nexu_run/.nexu/capsules/demo/src/src/demo.py:
    e: plan_demo
    plan_demo(user_goal)
  examples/mcp_service/.tmp_nexu_run/src/demo.py:
    e: plan_demo
    plan_demo(user_goal)
  examples/mcp_service/src/demo.py:
    e: plan_demo
    plan_demo(user_goal)
  examples/run_examples.py:
    e: run_example,main
    run_example(example)
    main()
  examples/vertical_slice/.tmp_nexu_run/.nexu/capsules/demo/src/src/flow.py:
    e: run_flow
    run_flow(menu_items)
  examples/vertical_slice/.tmp_nexu_run/src/flow.py:
    e: run_flow
    run_flow(menu_items)
  examples/vertical_slice/src/flow.py:
    e: run_flow
    run_flow(menu_items)
  src/nexu/__init__.py:
  src/nexu/__main__.py:
  src/nexu/blueprint.py:
    e: build_blueprint
    build_blueprint(root;name)
  src/nexu/bundle.py:
    e: _should_include,build_capsule_bundle
    _should_include(path;base)
    build_capsule_bundle(root;name)
  src/nexu/capsule.py:
    e: default_contract_manifest,create_capsule,list_capsules,load_capsule,save_capsule
    default_contract_manifest(capsule)
    create_capsule(root;name)
    list_capsules(root)
    load_capsule(root;name)
    save_capsule(root;capsule)
  src/nexu/cli.py:
    e: init,freeze,capsule_create,capsule_list,capsule_status_command,capsule_iterate,capsule_blueprint,capsule_export_prompt,capsule_diff,capsule_drift,capsule_verify,capsule_plan,capsule_runtime,capsule_report,capsule_journal,capsule_orchestrate,capsule_review,capsule_bundle,capsule_promote,mcp_tools,mcp_serve
    init(path)
    freeze(path;name;include)
    capsule_create(path;name;domain;include;route;endpoint;snapshot)
    capsule_list(path)
    capsule_status_command(name;path)
    capsule_iterate(name;path;steps;goal)
    capsule_blueprint(name;path;print_yaml)
    capsule_export_prompt(name;path;iteration)
    capsule_diff(name;path)
    capsule_drift(name;path)
    capsule_verify(name;path)
    capsule_plan(name;path;steps;goal;print_yaml)
    capsule_runtime(name;path)
    capsule_report(name;path)
    capsule_journal(name;path;limit)
    capsule_orchestrate(name;path;steps;goal;call_llm;model)
    capsule_review(name;path;iteration;call_llm;model)
    capsule_bundle(name;path;include_src)
    capsule_promote(name;path;dry_run)
    mcp_tools()
    mcp_serve(path;transport)
  src/nexu/config.py:
    e: _as_list,load_config,LLMConfig,ReviewConfig,nexuConfig
    LLMConfig:
    ReviewConfig:
    nexuConfig:
    _as_list(value;default)
    load_config(root)
  src/nexu/diff.py:
    e: diff_capsule
    diff_capsule(root;name)
  src/nexu/drift.py:
    e: check_source_drift
    check_source_drift(root;name)
  src/nexu/export_prompt.py:
    e: _latest_iteration,export_iteration_prompt
    _latest_iteration(capsule)
    export_iteration_prompt(root;name)
  src/nexu/files.py:
    e: rel,matches_any,is_text_file,collect_files
    rel(path;root)
    matches_any(value;patterns)
    is_text_file(path)
    collect_files(root;include;exclude)
  src/nexu/freeze.py:
    e: freeze_project
    freeze_project(root;name;include)
  src/nexu/git.py:
    e: current_git_sha
    current_git_sha(root)
  src/nexu/hashing.py:
    e: sha256_file,sha256_text
    sha256_file(path)
    sha256_text(text)
  src/nexu/init_project.py:
    e: init_project
    init_project(root)
  src/nexu/intract.py:
    e: _split_csv,_tokenize_contract,parse_intract_line,scan_contracts_in_text,scan_contracts_in_file,read_manifest_contracts,IntentContract
    IntentContract: key(0)
    _split_csv(value)
    _tokenize_contract(line)
    parse_intract_line(line)
    scan_contracts_in_text(text)
    scan_contracts_in_file(path;root)
    read_manifest_contracts(path)
  src/nexu/iterate.py:
    e: iterate_capsule
    iterate_capsule(root;name)
  src/nexu/journal.py:
    e: journal_path,read_journal,append_journal
    journal_path(root;name)
    read_journal(root;name)
    append_journal(root;name;event;message)
  src/nexu/llm.py:
    e: _extract_content,_strip_fences,call_litellm_json,offline_review_from_status,call_litellm_review
    _extract_content(response)
    _strip_fences(content)
    call_litellm_json(prompt)
    offline_review_from_status(status;score)
    call_litellm_review(prompt)
  src/nexu/mcp_server.py:
    e: _schema,_tool_map,call_tool,_result_content,_resource_list,_read_resource,_prompts_list,_prompt_get,handle_mcp_message,run_mcp_stdio
    _schema(properties;required)
    _tool_map(root)
    call_tool(root;tool_name;arguments)
    _result_content(data)
    _resource_list(root)
    _read_resource(root;uri)
    _prompts_list()
    _prompt_get(name;arguments)
    handle_mcp_message(root;message)
    run_mcp_stdio(root)
  src/nexu/models.py:
    e: utc_now,write_yaml,read_yaml,FrozenFile,FrozenSnapshot,CapsuleSelection,CapsuleRuntime,Capsule,VerificationFinding,VerificationReport,CapsuleDiff,PromptExport
    FrozenFile:
    FrozenSnapshot: to_dict(0),from_dict(2)
    CapsuleSelection:
    CapsuleRuntime:
    Capsule: to_dict(0),from_dict(2)
    VerificationFinding:
    VerificationReport: to_dict(0)
    CapsuleDiff: to_dict(0)
    PromptExport: to_dict(0)
    utc_now()
    write_yaml(path;data)
    read_yaml(path)
  src/nexu/orchestrate.py:
    e: _contract_dicts,build_orchestration_context,build_orchestration_prompt,offline_orchestration_from_context,build_capsule_orchestration,_render_orchestration_markdown
    _contract_dicts(contracts)
    build_orchestration_context(root;name)
    build_orchestration_prompt(context)
    offline_orchestration_from_context(context)
    build_capsule_orchestration(root;name)
    _render_orchestration_markdown(orchestration)
  src/nexu/paths.py:
    e: project_root,nexu_dir,snapshots_dir,capsules_dir,capsule_dir,ensure_project_dirs
    project_root(path)
    nexu_dir(root)
    snapshots_dir(root)
    capsules_dir(root)
    capsule_dir(root;name)
    ensure_project_dirs(root)
  src/nexu/plan.py:
    e: _contract_summary,build_iteration_plan
    _contract_summary(contracts)
    build_iteration_plan(root;name)
  src/nexu/promote.py:
    e: _promotion_map,build_promotion_plan
    _promotion_map(base;root;files)
    build_promotion_plan(root;name)
  src/nexu/report.py:
    e: _finding_table,_html_from_markdownish,build_capsule_report
    _finding_table(findings)
    _html_from_markdownish(title;markdown)
    build_capsule_report(root;name)
  src/nexu/review.py:
    e: _markdown_review_prompt,build_review_packet
    _markdown_review_prompt(packet)
    build_review_packet(root;name)
  src/nexu/runtime.py:
    e: _read_fixture,_collect_fixtures,_html_page,build_capsule_runtime
    _read_fixture(path)
    _collect_fixtures(base)
    _html_page(name;data)
    build_capsule_runtime(root;name)
  src/nexu/status.py:
    e: capsule_status
    capsule_status(root;name)
  src/nexu/verify.py:
    e: _scan_capsule_contracts,_text,_contains_patterns,_find_term_evidence,verify_capsule
    _scan_capsule_contracts(base;manifest_name)
    _text(path)
    _contains_patterns(path;patterns)
    _find_term_evidence(source_files;base;terms)
    verify_capsule(root;name)
  tests/test_capsule_flow.py:
    e: test_capsule_flow
    test_capsule_flow(tmp_path)
  tests/test_capsule_next_stage.py:
    e: test_capsule_blueprint_prompt_diff_status_and_drift
    test_capsule_blueprint_prompt_diff_status_and_drift(tmp_path)
  tests/test_capsule_runtime_report.py:
    e: test_plan_runtime_report_and_journal
    test_plan_runtime_report_and_journal(tmp_path)
  tests/test_intract.py:
    e: test_parse_intract_line
    test_parse_intract_line()
  tests/test_models.py:
    e: test_capsule_roundtrip,test_snapshot_roundtrip
    test_capsule_roundtrip()
    test_snapshot_roundtrip()
  tests/test_nexu.py:
    e: test_placeholder,test_import
    test_placeholder()
    test_import()
  tests/test_orchestration_mcp.py:
    e: _make_project,test_orchestration_offline,test_mcp_tool_dispatch_and_protocol
    _make_project(tmp_path)
    test_orchestration_offline(tmp_path)
    test_mcp_tool_dispatch_and_protocol(tmp_path)
  tests/test_review_bundle.py:
    e: test_review_bundle_and_promotion_prechecks
    test_review_bundle_and_promotion_prechecks(tmp_path)
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('nexu', '0.5.2', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 39, 'less').
project_file('examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/src/app/users.py', 9, 'python').
project_file('examples/backend_service/.tmp_nexu_run/app/users.py', 9, 'python').
project_file('examples/backend_service/app/users.py', 9, 'python').
project_file('examples/frontend_view/.tmp_nexu_run/.nexu/capsules/demo/src/src/menu_icons.py', 25, 'python').
project_file('examples/frontend_view/.tmp_nexu_run/src/menu_icons.py', 25, 'python').
project_file('examples/frontend_view/src/menu_icons.py', 25, 'python').
project_file('examples/mcp_service/.tmp_nexu_run/.nexu/capsules/demo/src/src/demo.py', 11, 'python').
project_file('examples/mcp_service/.tmp_nexu_run/src/demo.py', 11, 'python').
project_file('examples/mcp_service/src/demo.py', 11, 'python').
project_file('examples/run_examples.py', 80, 'python').
project_file('examples/vertical_slice/.tmp_nexu_run/.nexu/capsules/demo/src/src/flow.py', 10, 'python').
project_file('examples/vertical_slice/.tmp_nexu_run/src/flow.py', 10, 'python').
project_file('examples/vertical_slice/src/flow.py', 10, 'python').
project_file('project.sh', 50, 'shell').
project_file('src/nexu/__init__.py', 6, 'python').
project_file('src/nexu/__main__.py', 5, 'python').
project_file('src/nexu/blueprint.py', 74, 'python').
project_file('src/nexu/bundle.py', 56, 'python').
project_file('src/nexu/capsule.py', 125, 'python').
project_file('src/nexu/cli.py', 358, 'python').
project_file('src/nexu/config.py', 78, 'python').
project_file('src/nexu/diff.py', 36, 'python').
project_file('src/nexu/drift.py', 37, 'python').
project_file('src/nexu/export_prompt.py', 101, 'python').
project_file('src/nexu/files.py', 52, 'python').
project_file('src/nexu/freeze.py', 27, 'python').
project_file('src/nexu/git.py', 23, 'python').
project_file('src/nexu/hashing.py', 17, 'python').
project_file('src/nexu/init_project.py', 87, 'python').
project_file('src/nexu/intract.py', 126, 'python').
project_file('src/nexu/iterate.py', 45, 'python').
project_file('src/nexu/journal.py', 44, 'python').
project_file('src/nexu/llm.py', 166, 'python').
project_file('src/nexu/mcp_server.py', 356, 'python').
project_file('src/nexu/models.py', 155, 'python').
project_file('src/nexu/orchestrate.py', 233, 'python').
project_file('src/nexu/paths.py', 36, 'python').
project_file('src/nexu/plan.py', 82, 'python').
project_file('src/nexu/promote.py', 78, 'python').
project_file('src/nexu/report.py', 95, 'python').
project_file('src/nexu/review.py', 158, 'python').
project_file('src/nexu/runtime.py', 132, 'python').
project_file('src/nexu/status.py', 36, 'python').
project_file('src/nexu/verify.py', 237, 'python').
project_file('tests/test_capsule_flow.py', 26, 'python').
project_file('tests/test_capsule_next_stage.py', 59, 'python').
project_file('tests/test_capsule_runtime_report.py', 51, 'python').
project_file('tests/test_intract.py', 12, 'python').
project_file('tests/test_models.py', 15, 'python').
project_file('tests/test_nexu.py', 12, 'python').
project_file('tests/test_orchestration_mcp.py', 63, 'python').
project_file('tests/test_review_bundle.py', 46, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/src/app/users.py', 'list_users', 2, 4, 1).
python_function('examples/backend_service/.tmp_nexu_run/app/users.py', 'list_users', 2, 4, 1).
python_function('examples/backend_service/app/users.py', 'list_users', 2, 4, 1).
python_function('examples/frontend_view/.tmp_nexu_run/.nexu/capsules/demo/src/src/menu_icons.py', 'preview_menu_icons', 1, 3, 2).
python_function('examples/frontend_view/.tmp_nexu_run/src/menu_icons.py', 'preview_menu_icons', 1, 3, 2).
python_function('examples/frontend_view/src/menu_icons.py', 'preview_menu_icons', 1, 3, 2).
python_function('examples/mcp_service/.tmp_nexu_run/.nexu/capsules/demo/src/src/demo.py', 'plan_demo', 1, 1, 0).
python_function('examples/mcp_service/.tmp_nexu_run/src/demo.py', 'plan_demo', 1, 1, 0).
python_function('examples/mcp_service/src/demo.py', 'plan_demo', 1, 1, 0).
python_function('examples/run_examples.py', 'run_example', 1, 2, 23).
python_function('examples/run_examples.py', 'main', 0, 2, 1).
python_function('examples/vertical_slice/.tmp_nexu_run/.nexu/capsules/demo/src/src/flow.py', 'run_flow', 1, 1, 0).
python_function('examples/vertical_slice/.tmp_nexu_run/src/flow.py', 'run_flow', 1, 1, 0).
python_function('examples/vertical_slice/src/flow.py', 'run_flow', 1, 1, 0).
python_function('src/nexu/blueprint.py', 'build_blueprint', 2, 7, 7).
python_function('src/nexu/bundle.py', '_should_include', 2, 5, 3).
python_function('src/nexu/bundle.py', 'build_capsule_bundle', 2, 3, 14).
python_function('src/nexu/capsule.py', 'default_contract_manifest', 1, 1, 1).
python_function('src/nexu/capsule.py', 'create_capsule', 2, 8, 20).
python_function('src/nexu/capsule.py', 'list_capsules', 1, 4, 5).
python_function('src/nexu/capsule.py', 'load_capsule', 2, 1, 3).
python_function('src/nexu/capsule.py', 'save_capsule', 2, 1, 3).
python_function('src/nexu/cli.py', 'init', 1, 3, 6).
python_function('src/nexu/cli.py', 'freeze', 3, 2, 7).
python_function('src/nexu/cli.py', 'capsule_create', 7, 1, 8).
python_function('src/nexu/cli.py', 'capsule_list', 1, 3, 7).
python_function('src/nexu/cli.py', 'capsule_status_command', 2, 3, 11).
python_function('src/nexu/cli.py', 'capsule_iterate', 4, 1, 9).
python_function('src/nexu/cli.py', 'capsule_blueprint', 3, 2, 8).
python_function('src/nexu/cli.py', 'capsule_export_prompt', 3, 1, 8).
python_function('src/nexu/cli.py', 'capsule_diff', 2, 1, 10).
python_function('src/nexu/cli.py', 'capsule_drift', 2, 2, 7).
python_function('src/nexu/cli.py', 'capsule_verify', 2, 4, 8).
python_function('src/nexu/cli.py', 'capsule_plan', 5, 2, 9).
python_function('src/nexu/cli.py', 'capsule_runtime', 2, 1, 8).
python_function('src/nexu/cli.py', 'capsule_report', 2, 1, 8).
python_function('src/nexu/cli.py', 'capsule_journal', 3, 2, 10).
python_function('src/nexu/cli.py', 'capsule_orchestrate', 6, 1, 8).
python_function('src/nexu/cli.py', 'capsule_review', 5, 1, 8).
python_function('src/nexu/cli.py', 'capsule_bundle', 3, 1, 8).
python_function('src/nexu/cli.py', 'capsule_promote', 3, 2, 7).
python_function('src/nexu/cli.py', 'mcp_tools', 0, 2, 6).
python_function('src/nexu/cli.py', 'mcp_serve', 2, 2, 5).
python_function('src/nexu/config.py', '_as_list', 2, 4, 2).
python_function('src/nexu/config.py', 'load_config', 1, 6, 12).
python_function('src/nexu/diff.py', 'diff_capsule', 2, 12, 10).
python_function('src/nexu/drift.py', 'check_source_drift', 2, 7, 9).
python_function('src/nexu/export_prompt.py', '_latest_iteration', 1, 2, 0).
python_function('src/nexu/export_prompt.py', 'export_iteration_prompt', 2, 3, 14).
python_function('src/nexu/files.py', 'rel', 2, 1, 2).
python_function('src/nexu/files.py', 'matches_any', 2, 3, 3).
python_function('src/nexu/files.py', 'is_text_file', 1, 2, 1).
python_function('src/nexu/files.py', 'collect_files', 3, 8, 7).
python_function('src/nexu/freeze.py', 'freeze_project', 3, 2, 12).
python_function('src/nexu/git.py', 'current_git_sha', 1, 4, 3).
python_function('src/nexu/hashing.py', 'sha256_file', 1, 2, 6).
python_function('src/nexu/hashing.py', 'sha256_text', 1, 1, 3).
python_function('src/nexu/init_project.py', 'init_project', 1, 3, 4).
python_function('src/nexu/intract.py', '_split_csv', 1, 4, 3).
python_function('src/nexu/intract.py', '_tokenize_contract', 1, 5, 6).
python_function('src/nexu/intract.py', 'parse_intract_line', 1, 3, 6).
python_function('src/nexu/intract.py', 'scan_contracts_in_text', 1, 3, 4).
python_function('src/nexu/intract.py', 'scan_contracts_in_file', 2, 3, 4).
python_function('src/nexu/intract.py', 'read_manifest_contracts', 1, 12, 9).
python_function('src/nexu/iterate.py', 'iterate_capsule', 2, 7, 13).
python_function('src/nexu/journal.py', 'journal_path', 2, 1, 1).
python_function('src/nexu/journal.py', 'read_journal', 2, 5, 5).
python_function('src/nexu/journal.py', 'append_journal', 4, 2, 6).
python_function('src/nexu/llm.py', '_extract_content', 1, 4, 3).
python_function('src/nexu/llm.py', '_strip_fences', 1, 7, 4).
python_function('src/nexu/llm.py', 'call_litellm_json', 1, 8, 8).
python_function('src/nexu/llm.py', 'offline_review_from_status', 2, 4, 0).
python_function('src/nexu/llm.py', 'call_litellm_review', 1, 2, 2).
python_function('src/nexu/mcp_server.py', '_schema', 2, 2, 0).
python_function('src/nexu/mcp_server.py', '_tool_map', 1, 10, 20).
python_function('src/nexu/mcp_server.py', 'call_tool', 3, 3, 2).
python_function('src/nexu/mcp_server.py', '_result_content', 1, 1, 1).
python_function('src/nexu/mcp_server.py', '_resource_list', 1, 2, 2).
python_function('src/nexu/mcp_server.py', '_read_resource', 2, 6, 9).
python_function('src/nexu/mcp_server.py', '_prompts_list', 0, 1, 0).
python_function('src/nexu/mcp_server.py', '_prompt_get', 2, 3, 2).
python_function('src/nexu/mcp_server.py', 'handle_mcp_message', 2, 14, 8).
python_function('src/nexu/mcp_server.py', 'run_mcp_stdio', 1, 6, 7).
python_function('src/nexu/models.py', 'utc_now', 0, 1, 2).
python_function('src/nexu/models.py', 'write_yaml', 2, 1, 3).
python_function('src/nexu/models.py', 'read_yaml', 1, 3, 4).
python_function('src/nexu/orchestrate.py', '_contract_dicts', 1, 2, 0).
python_function('src/nexu/orchestrate.py', 'build_orchestration_context', 2, 2, 9).
python_function('src/nexu/orchestrate.py', 'build_orchestration_prompt', 1, 1, 1).
python_function('src/nexu/orchestrate.py', 'offline_orchestration_from_context', 1, 13, 6).
python_function('src/nexu/orchestrate.py', 'build_capsule_orchestration', 2, 2, 16).
python_function('src/nexu/orchestrate.py', '_render_orchestration_markdown', 1, 9, 4).
python_function('src/nexu/paths.py', 'project_root', 1, 1, 3).
python_function('src/nexu/paths.py', 'nexu_dir', 1, 1, 0).
python_function('src/nexu/paths.py', 'snapshots_dir', 1, 1, 1).
python_function('src/nexu/paths.py', 'capsules_dir', 1, 1, 1).
python_function('src/nexu/paths.py', 'capsule_dir', 2, 1, 1).
python_function('src/nexu/paths.py', 'ensure_project_dirs', 1, 2, 4).
python_function('src/nexu/plan.py', '_contract_summary', 1, 9, 1).
python_function('src/nexu/plan.py', 'build_iteration_plan', 2, 7, 15).
python_function('src/nexu/promote.py', '_promotion_map', 3, 2, 3).
python_function('src/nexu/promote.py', 'build_promotion_plan', 2, 6, 14).
python_function('src/nexu/report.py', '_finding_table', 1, 2, 5).
python_function('src/nexu/report.py', '_html_from_markdownish', 2, 1, 1).
python_function('src/nexu/report.py', 'build_capsule_report', 2, 1, 18).
python_function('src/nexu/review.py', '_markdown_review_prompt', 1, 1, 1).
python_function('src/nexu/review.py', 'build_review_packet', 2, 5, 19).
python_function('src/nexu/runtime.py', '_read_fixture', 1, 5, 5).
python_function('src/nexu/runtime.py', '_collect_fixtures', 1, 5, 7).
python_function('src/nexu/runtime.py', '_html_page', 2, 9, 5).
python_function('src/nexu/runtime.py', 'build_capsule_runtime', 2, 3, 13).
python_function('src/nexu/status.py', 'capsule_status', 2, 3, 6).
python_function('src/nexu/verify.py', '_scan_capsule_contracts', 2, 2, 4).
python_function('src/nexu/verify.py', '_text', 1, 2, 1).
python_function('src/nexu/verify.py', '_contains_patterns', 2, 3, 2).
python_function('src/nexu/verify.py', '_find_term_evidence', 3, 6, 8).
python_function('src/nexu/verify.py', 'verify_capsule', 2, 45, 23).
python_function('tests/test_capsule_flow.py', 'test_capsule_flow', 1, 5, 7).
python_function('tests/test_capsule_next_stage.py', 'test_capsule_blueprint_prompt_diff_status_and_drift', 1, 11, 14).
python_function('tests/test_capsule_runtime_report.py', 'test_plan_runtime_report_and_journal', 1, 13, 13).
python_function('tests/test_intract.py', 'test_parse_intract_line', 0, 5, 1).
python_function('tests/test_models.py', 'test_capsule_roundtrip', 0, 3, 4).
python_function('tests/test_models.py', 'test_snapshot_roundtrip', 0, 2, 3).
python_function('tests/test_nexu.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_nexu.py', 'test_import', 0, 1, 0).
python_function('tests/test_orchestration_mcp.py', '_make_project', 1, 1, 2).
python_function('tests/test_orchestration_mcp.py', 'test_orchestration_offline', 1, 5, 6).
python_function('tests/test_orchestration_mcp.py', 'test_mcp_tool_dispatch_and_protocol', 1, 7, 5).
python_function('tests/test_review_bundle.py', 'test_review_bundle_and_promotion_prechecks', 1, 13, 14).

% ── Python Classes ───────────────────────────────────────
python_class('src/nexu/config.py', 'LLMConfig').
python_class('src/nexu/config.py', 'ReviewConfig').
python_class('src/nexu/config.py', 'nexuConfig').
python_class('src/nexu/intract.py', 'IntentContract').
python_method('IntentContract', 'key', 0, 3, 0).
python_class('src/nexu/models.py', 'FrozenFile').
python_class('src/nexu/models.py', 'FrozenSnapshot').
python_method('FrozenSnapshot', 'to_dict', 0, 1, 1).
python_method('FrozenSnapshot', 'from_dict', 2, 2, 4).
python_class('src/nexu/models.py', 'CapsuleSelection').
python_class('src/nexu/models.py', 'CapsuleRuntime').
python_class('src/nexu/models.py', 'Capsule').
python_method('Capsule', 'to_dict', 0, 1, 1).
python_method('Capsule', 'from_dict', 2, 2, 7).
python_class('src/nexu/models.py', 'VerificationFinding').
python_class('src/nexu/models.py', 'VerificationReport').
python_method('VerificationReport', 'to_dict', 0, 1, 1).
python_class('src/nexu/models.py', 'CapsuleDiff').
python_method('CapsuleDiff', 'to_dict', 0, 1, 1).
python_class('src/nexu/models.py', 'PromptExport').
python_method('PromptExport', 'to_dict', 0, 1, 1).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('test', '').
makefile_target('examples', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'pytest -q').
sumd_workflow('examples', 'manual').
sumd_workflow_step('examples', 1, 'python examples/run_examples.py').
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

## Intent

Visual Intent Contract Orchestrator: freeze project slices, evolve capsules, verify intent contracts.
