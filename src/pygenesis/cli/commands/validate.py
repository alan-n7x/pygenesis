from __future__ import annotations

from pathlib import Path

import typer

from pygenesis.config.loader import ConfigLoader
from pygenesis.config.validator import ConfigValidator


def validate_cmd(
    config: Path = typer.Argument("pygenesis.yaml", help="Config file to validate"),  # noqa: B008
) -> None:
    config_path = Path(config)
    if not config_path.exists():
        typer.echo(f"Config file not found: {config_path}")
        raise typer.Exit(code=1)

    try:
        proj_config = ConfigLoader.load(config_path)
    except Exception as exc:
        typer.echo(f"Config parse error: {exc}")
        raise typer.Exit(code=1) from exc

    errors = ConfigValidator.validate(proj_config)
    if errors:
        typer.echo(f"Config validation failed ({len(errors)} errors):")
        for err in errors:
            typer.echo(f"  ✗ {err}")
        raise typer.Exit(code=1)

    typer.echo("✓ Config is valid")
