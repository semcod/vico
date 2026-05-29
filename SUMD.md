# Vico

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
- **version**: `0.2.5`
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

## Interfaces

### CLI Entry Points

- `vico`

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
  version: 0.2.5
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
# nexu | 32f 1775L | python:29,shell:2,less:1 | 2026-05-29
# stats: 66 func | 10 cls | 32 mod | CC̄=3.8 | critical:4 | cycles:0
# alerts[5]: CC verify_capsule=45; CC diff_capsule=12; CC read_manifest_contracts=12; CC test_capsule_blueprint_prompt_diff_status_and_drift=11; CC create_capsule=8
# hotspots[5]: verify_capsule fan=23; create_capsule fan=19; run_example fan=17; export_iteration_prompt fan=14; test_capsule_blueprint_prompt_diff_status_and_drift fan=14
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[32]:
  app.doql.less,39
  examples/backend_service/app/users.py,9
  examples/frontend_view/src/menu_icons.py,25
  examples/run_examples.py,65
  examples/vertical_slice/src/flow.py,10
  project.sh,50
  src/vico/__init__.py,6
  src/vico/__main__.py,5
  src/vico/blueprint.py,74
  src/vico/capsule.py,123
  src/vico/cli.py,220
  src/vico/diff.py,36
  src/vico/drift.py,37
  src/vico/export_prompt.py,101
  src/vico/files.py,52
  src/vico/freeze.py,27
  src/vico/git.py,23
  src/vico/hashing.py,17
  src/vico/init_project.py,63
  src/vico/intract.py,126
  src/vico/iterate.py,45
  src/vico/models.py,155
  src/vico/paths.py,36
  src/vico/promote.py,32
  src/vico/status.py,36
  src/vico/verify.py,237
  tests/test_capsule_flow.py,26
  tests/test_capsule_next_stage.py,59
  tests/test_intract.py,12
  tests/test_models.py,15
  tests/test_vico.py,12
  tree.sh,2
D:
  examples/backend_service/app/users.py:
    e: list_users
    list_users(filters;users)
  examples/frontend_view/src/menu_icons.py:
    e: preview_menu_icons
    preview_menu_icons(menu_items)
  examples/run_examples.py:
    e: run_example,main
    run_example(example)
    main()
  examples/vertical_slice/src/flow.py:
    e: run_flow
    run_flow(menu_items)
  src/vico/__init__.py:
  src/vico/__main__.py:
  src/vico/blueprint.py:
    e: build_blueprint
    build_blueprint(root;name)
  src/vico/capsule.py:
    e: default_contract_manifest,create_capsule,list_capsules,load_capsule,save_capsule
    default_contract_manifest(capsule)
    create_capsule(root;name)
    list_capsules(root)
    load_capsule(root;name)
    save_capsule(root;capsule)
  src/vico/cli.py:
    e: init,freeze,capsule_create,capsule_list,capsule_status_command,capsule_iterate,capsule_blueprint,capsule_export_prompt,capsule_diff,capsule_drift,capsule_verify,capsule_promote
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
    capsule_promote(name;path;dry_run)
  src/vico/diff.py:
    e: diff_capsule
    diff_capsule(root;name)
  src/vico/drift.py:
    e: check_source_drift
    check_source_drift(root;name)
  src/vico/export_prompt.py:
    e: _latest_iteration,export_iteration_prompt
    _latest_iteration(capsule)
    export_iteration_prompt(root;name)
  src/vico/files.py:
    e: rel,matches_any,is_text_file,collect_files
    rel(path;root)
    matches_any(value;patterns)
    is_text_file(path)
    collect_files(root;include;exclude)
  src/vico/freeze.py:
    e: freeze_project
    freeze_project(root;name;include)
  src/vico/git.py:
    e: current_git_sha
    current_git_sha(root)
  src/vico/hashing.py:
    e: sha256_file,sha256_text
    sha256_file(path)
    sha256_text(text)
  src/vico/init_project.py:
    e: init_project
    init_project(root)
  src/vico/intract.py:
    e: _split_csv,_tokenize_contract,parse_intract_line,scan_contracts_in_text,scan_contracts_in_file,read_manifest_contracts,IntentContract
    IntentContract: key(0)
    _split_csv(value)
    _tokenize_contract(line)
    parse_intract_line(line)
    scan_contracts_in_text(text)
    scan_contracts_in_file(path;root)
    read_manifest_contracts(path)
  src/vico/iterate.py:
    e: iterate_capsule
    iterate_capsule(root;name)
  src/vico/models.py:
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
  src/vico/paths.py:
    e: project_root,vico_dir,snapshots_dir,capsules_dir,capsule_dir,ensure_project_dirs
    project_root(path)
    vico_dir(root)
    snapshots_dir(root)
    capsules_dir(root)
    capsule_dir(root;name)
    ensure_project_dirs(root)
  src/vico/promote.py:
    e: build_promotion_plan
    build_promotion_plan(root;name)
  src/vico/status.py:
    e: capsule_status
    capsule_status(root;name)
  src/vico/verify.py:
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
  tests/test_intract.py:
    e: test_parse_intract_line
    test_parse_intract_line()
  tests/test_models.py:
    e: test_capsule_roundtrip,test_snapshot_roundtrip
    test_capsule_roundtrip()
    test_snapshot_roundtrip()
  tests/test_vico.py:
    e: test_placeholder,test_import
    test_placeholder()
    test_import()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('nexu', '0.2.5', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 39, 'less').
project_file('examples/backend_service/app/users.py', 9, 'python').
project_file('examples/frontend_view/src/menu_icons.py', 25, 'python').
project_file('examples/run_examples.py', 65, 'python').
project_file('examples/vertical_slice/src/flow.py', 10, 'python').
project_file('project.sh', 50, 'shell').
project_file('src/vico/__init__.py', 6, 'python').
project_file('src/vico/__main__.py', 5, 'python').
project_file('src/vico/blueprint.py', 74, 'python').
project_file('src/vico/capsule.py', 123, 'python').
project_file('src/vico/cli.py', 220, 'python').
project_file('src/vico/diff.py', 36, 'python').
project_file('src/vico/drift.py', 37, 'python').
project_file('src/vico/export_prompt.py', 101, 'python').
project_file('src/vico/files.py', 52, 'python').
project_file('src/vico/freeze.py', 27, 'python').
project_file('src/vico/git.py', 23, 'python').
project_file('src/vico/hashing.py', 17, 'python').
project_file('src/vico/init_project.py', 63, 'python').
project_file('src/vico/intract.py', 126, 'python').
project_file('src/vico/iterate.py', 45, 'python').
project_file('src/vico/models.py', 155, 'python').
project_file('src/vico/paths.py', 36, 'python').
project_file('src/vico/promote.py', 32, 'python').
project_file('src/vico/status.py', 36, 'python').
project_file('src/vico/verify.py', 237, 'python').
project_file('tests/test_capsule_flow.py', 26, 'python').
project_file('tests/test_capsule_next_stage.py', 59, 'python').
project_file('tests/test_intract.py', 12, 'python').
project_file('tests/test_models.py', 15, 'python').
project_file('tests/test_vico.py', 12, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/backend_service/app/users.py', 'list_users', 2, 4, 1).
python_function('examples/frontend_view/src/menu_icons.py', 'preview_menu_icons', 1, 3, 2).
python_function('examples/run_examples.py', 'run_example', 1, 2, 17).
python_function('examples/run_examples.py', 'main', 0, 2, 1).
python_function('examples/vertical_slice/src/flow.py', 'run_flow', 1, 1, 0).
python_function('src/vico/blueprint.py', 'build_blueprint', 2, 7, 7).
python_function('src/vico/capsule.py', 'default_contract_manifest', 1, 1, 1).
python_function('src/vico/capsule.py', 'create_capsule', 2, 8, 19).
python_function('src/vico/capsule.py', 'list_capsules', 1, 4, 5).
python_function('src/vico/capsule.py', 'load_capsule', 2, 1, 3).
python_function('src/vico/capsule.py', 'save_capsule', 2, 1, 3).
python_function('src/vico/cli.py', 'init', 1, 3, 6).
python_function('src/vico/cli.py', 'freeze', 3, 2, 7).
python_function('src/vico/cli.py', 'capsule_create', 7, 1, 8).
python_function('src/vico/cli.py', 'capsule_list', 1, 3, 7).
python_function('src/vico/cli.py', 'capsule_status_command', 2, 3, 11).
python_function('src/vico/cli.py', 'capsule_iterate', 4, 1, 7).
python_function('src/vico/cli.py', 'capsule_blueprint', 3, 2, 8).
python_function('src/vico/cli.py', 'capsule_export_prompt', 3, 1, 8).
python_function('src/vico/cli.py', 'capsule_diff', 2, 1, 10).
python_function('src/vico/cli.py', 'capsule_drift', 2, 2, 7).
python_function('src/vico/cli.py', 'capsule_verify', 2, 4, 8).
python_function('src/vico/cli.py', 'capsule_promote', 3, 2, 7).
python_function('src/vico/diff.py', 'diff_capsule', 2, 12, 10).
python_function('src/vico/drift.py', 'check_source_drift', 2, 7, 9).
python_function('src/vico/export_prompt.py', '_latest_iteration', 1, 2, 0).
python_function('src/vico/export_prompt.py', 'export_iteration_prompt', 2, 3, 14).
python_function('src/vico/files.py', 'rel', 2, 1, 2).
python_function('src/vico/files.py', 'matches_any', 2, 3, 3).
python_function('src/vico/files.py', 'is_text_file', 1, 2, 1).
python_function('src/vico/files.py', 'collect_files', 3, 8, 7).
python_function('src/vico/freeze.py', 'freeze_project', 3, 2, 12).
python_function('src/vico/git.py', 'current_git_sha', 1, 4, 3).
python_function('src/vico/hashing.py', 'sha256_file', 1, 2, 6).
python_function('src/vico/hashing.py', 'sha256_text', 1, 1, 3).
python_function('src/vico/init_project.py', 'init_project', 1, 3, 4).
python_function('src/vico/intract.py', '_split_csv', 1, 4, 3).
python_function('src/vico/intract.py', '_tokenize_contract', 1, 5, 6).
python_function('src/vico/intract.py', 'parse_intract_line', 1, 3, 6).
python_function('src/vico/intract.py', 'scan_contracts_in_text', 1, 3, 4).
python_function('src/vico/intract.py', 'scan_contracts_in_file', 2, 3, 4).
python_function('src/vico/intract.py', 'read_manifest_contracts', 1, 12, 9).
python_function('src/vico/iterate.py', 'iterate_capsule', 2, 7, 13).
python_function('src/vico/models.py', 'utc_now', 0, 1, 2).
python_function('src/vico/models.py', 'write_yaml', 2, 1, 3).
python_function('src/vico/models.py', 'read_yaml', 1, 3, 4).
python_function('src/vico/paths.py', 'project_root', 1, 1, 3).
python_function('src/vico/paths.py', 'vico_dir', 1, 1, 0).
python_function('src/vico/paths.py', 'snapshots_dir', 1, 1, 1).
python_function('src/vico/paths.py', 'capsules_dir', 1, 1, 1).
python_function('src/vico/paths.py', 'capsule_dir', 2, 1, 1).
python_function('src/vico/paths.py', 'ensure_project_dirs', 1, 2, 4).
python_function('src/vico/promote.py', 'build_promotion_plan', 2, 2, 6).
python_function('src/vico/status.py', 'capsule_status', 2, 3, 6).
python_function('src/vico/verify.py', '_scan_capsule_contracts', 2, 2, 4).
python_function('src/vico/verify.py', '_text', 1, 2, 1).
python_function('src/vico/verify.py', '_contains_patterns', 2, 3, 2).
python_function('src/vico/verify.py', '_find_term_evidence', 3, 6, 8).
python_function('src/vico/verify.py', 'verify_capsule', 2, 45, 23).
python_function('tests/test_capsule_flow.py', 'test_capsule_flow', 1, 5, 7).
python_function('tests/test_capsule_next_stage.py', 'test_capsule_blueprint_prompt_diff_status_and_drift', 1, 11, 14).
python_function('tests/test_intract.py', 'test_parse_intract_line', 0, 5, 1).
python_function('tests/test_models.py', 'test_capsule_roundtrip', 0, 3, 4).
python_function('tests/test_models.py', 'test_snapshot_roundtrip', 0, 2, 3).
python_function('tests/test_vico.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_vico.py', 'test_import', 0, 1, 0).

% ── Python Classes ───────────────────────────────────────
python_class('src/vico/intract.py', 'IntentContract').
python_method('IntentContract', 'key', 0, 3, 0).
python_class('src/vico/models.py', 'FrozenFile').
python_class('src/vico/models.py', 'FrozenSnapshot').
python_method('FrozenSnapshot', 'to_dict', 0, 1, 1).
python_method('FrozenSnapshot', 'from_dict', 2, 2, 4).
python_class('src/vico/models.py', 'CapsuleSelection').
python_class('src/vico/models.py', 'CapsuleRuntime').
python_class('src/vico/models.py', 'Capsule').
python_method('Capsule', 'to_dict', 0, 1, 1).
python_method('Capsule', 'from_dict', 2, 2, 7).
python_class('src/vico/models.py', 'VerificationFinding').
python_class('src/vico/models.py', 'VerificationReport').
python_method('VerificationReport', 'to_dict', 0, 1, 1).
python_class('src/vico/models.py', 'CapsuleDiff').
python_method('CapsuleDiff', 'to_dict', 0, 1, 1).
python_class('src/vico/models.py', 'PromptExport').
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

## Intent

Visual Intent Contract Orchestrator: freeze project slices, evolve capsules, verify intent contracts.
