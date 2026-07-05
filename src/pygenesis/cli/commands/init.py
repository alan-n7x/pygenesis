from __future__ import annotations

import typer


def init_cmd(
    name: str = typer.Argument("pygenesis.yaml", help="Config file to initialize"),
) -> None:
    typer.echo(f"init command not yet implemented: {name}")
