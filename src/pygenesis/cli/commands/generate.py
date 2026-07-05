from __future__ import annotations

from pathlib import Path

import typer


def generate_cmd(
    config: Path = typer.Option("pygenesis.toml", "--config", "-c", help="Config file"),  # noqa: B008
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show changes without writing"),  # noqa: B008
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),  # noqa: B008
) -> None:
    _ = force
    if not config.exists():
        typer.echo(f"  Config not found: {config}")
        raise typer.Exit(code=1)

    typer.echo("  [generate] Generation coming in Stage 4.")
    if dry_run:
        typer.echo("  (dry-run mode)")
