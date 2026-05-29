from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .capsule import create_capsule, list_capsules
from .freeze import freeze_project
from .init_project import init_project
from .iterate import iterate_capsule
from .paths import project_root
from .promote import build_promotion_plan
from .verify import verify_capsule

app = typer.Typer(help="Vico — Visual Intent Contract Orchestrator.")
capsule_app = typer.Typer(help="Create, iterate, verify and promote project capsules.")
app.add_typer(capsule_app, name="capsule")
console = Console()


@app.command()
def init(path: Annotated[str, typer.Argument(help="Project root.")] = ".") -> None:
    """Initialize Vico files in a project."""
    root = project_root(path)
    created = init_project(root)
    if not created:
        console.print("[green]Vico already initialized.[/green]")
        return
    for item in created:
        console.print(f"[green]created[/green] {item.relative_to(root)}")


@app.command()
def freeze(
    path: Annotated[str, typer.Argument(help="Project root.")] = ".",
    name: Annotated[str, typer.Option("--name", "-n", help="Snapshot name.")] = "baseline",
    include: Annotated[list[str] | None, typer.Option("--include", "-i", help="Glob include.")] = None,
) -> None:
    """Freeze a lightweight hash snapshot of the current project."""
    root = project_root(path)
    snapshot = freeze_project(root, name=name, include=include)
    console.print(f"[green]snapshot[/green] {snapshot.id}")
    console.print(f"files: {len(snapshot.files)}")
    if snapshot.git_sha:
        console.print(f"git: {snapshot.git_sha[:12]}")


@capsule_app.command("create")
def capsule_create(
    path: Annotated[str, typer.Argument(help="Project root.")] = ".",
    name: Annotated[str, typer.Option("--name", "-n", help="Capsule name.")] = "capsule",
    domain: Annotated[str, typer.Option("--domain", "-d", help="Domain name.")] = "general",
    include: Annotated[list[str] | None, typer.Option("--include", "-i", help="Glob include pattern.")] = None,
    route: Annotated[list[str] | None, typer.Option("--route", help="UI route covered by capsule.")] = None,
    endpoint: Annotated[list[str] | None, typer.Option("--endpoint", help="Endpoint covered by capsule.")] = None,
    snapshot: Annotated[str | None, typer.Option("--snapshot", help="Source snapshot id.")] = None,
) -> None:
    """Create an isolated capsule from selected project files."""
    root = project_root(path)
    capsule = create_capsule(
        root,
        name,
        domain=domain,
        include=include,
        routes=route,
        endpoints=endpoint,
        snapshot_id=snapshot,
    )
    console.print(f"[green]capsule created[/green] {capsule.name}")
    console.print(f"location: .vico/capsules/{capsule.name}")


@capsule_app.command("list")
def capsule_list(path: Annotated[str, typer.Argument(help="Project root.")] = ".") -> None:
    """List local capsules."""
    root = project_root(path)
    names = list_capsules(root)
    if not names:
        console.print("[yellow]No capsules found.[/yellow]")
        return
    table = Table("Capsule")
    for name in names:
        table.add_row(name)
    console.print(table)


@capsule_app.command("iterate")
def capsule_iterate(
    name: Annotated[str, typer.Argument(help="Capsule name.")],
    path: Annotated[str, typer.Option("--path", "-p", help="Project root.")] = ".",
    steps: Annotated[int, typer.Option("--steps", "-s", help="How many planned iterations to create.")] = 1,
    goal: Annotated[str, typer.Option("--goal", "-g", help="Iteration goal.")] = "Evolve capsule safely.",
) -> None:
    """Create planned S1..Sn iteration folders and prompts."""
    root = project_root(path)
    created = iterate_capsule(root, name, steps=steps, goal=goal)
    console.print(f"[green]created iterations[/green] {', '.join(created)}")


@capsule_app.command("verify")
def capsule_verify(
    name: Annotated[str, typer.Argument(help="Capsule name.")],
    path: Annotated[str, typer.Option("--path", "-p", help="Project root.")] = ".",
) -> None:
    """Verify a capsule against basic intent-contract gates."""
    root = project_root(path)
    report = verify_capsule(root, name)
    console.print(f"status: [{ 'green' if report.status == 'pass' else 'red' if report.status == 'fail' else 'yellow' }]{report.status}[/]")
    console.print(f"score: {report.score:.2f}")
    table = Table("Gate", "Status", "Message")
    for finding in report.findings:
        table.add_row(finding.code, finding.status, finding.message)
    console.print(table)


@capsule_app.command("promote")
def capsule_promote(
    name: Annotated[str, typer.Argument(help="Capsule name.")],
    path: Annotated[str, typer.Option("--path", "-p", help="Project root.")] = ".",
    dry_run: Annotated[bool, typer.Option("--dry-run/--apply", help="Only create a promotion plan.")] = True,
) -> None:
    """Build a promotion plan for copying capsule changes back to the source project."""
    root = project_root(path)
    plan = build_promotion_plan(root, name)
    console.print(f"[green]promotion plan[/green] .vico/capsules/{name}/promotion-plan.yaml")
    console.print(f"files to review: {len(plan['files_to_review'])}")
    if not dry_run:
        console.print("[yellow]Apply mode is intentionally not implemented in MVP. Review the plan first.[/yellow]")
