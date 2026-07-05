from __future__ import annotations

from pathlib import Path

import typer

from pygenesis.config.loader import ConfigLoader
from pygenesis.config.validator import ConfigValidator
from pygenesis.generators.project import ProjectGenerator


def new_cmd(
    name: str = typer.Argument(..., help="Project name"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output directory"),  # noqa: B008
    config: Path | None = typer.Option(None, "--config", "-c", help="Path to YAML config file"),  # noqa: B008
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing directory"),
) -> None:
    output_dir = Path(output or Path.cwd())
    project_dir = output_dir / name

    if project_dir.exists() and not force:
        typer.echo(f"Error: {project_dir} already exists. Use --force to overwrite.")
        raise typer.Exit(code=1)

    if config and config.exists():
        proj_config = ConfigLoader.load(config)
    else:
        typer.echo("No config file provided. Generating default config...")
        config_yaml = ConfigLoader.generate_default(
            name=name,
            owner="your-github-username",
            author_name="Your Name",
            author_email="your@email.com",
        )
        config_path = project_dir / "pygenesis.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config_yaml, encoding="utf-8")
        typer.echo(f"  Edit {config_path} with your info, then re-run.")
        proj_config = ConfigLoader.load(config_path)

    errors = ConfigValidator.validate(proj_config)
    if errors:
        for err in errors:
            typer.echo(f"  Config error: {err}")
        raise typer.Exit(code=1)

    generator = ProjectGenerator()
    generator.generate(proj_config, output_dir)

    typer.echo(f"Project created: {project_dir}")
    typer.echo(f"  cd {project_dir}")
    typer.echo("  git init && git add . && git commit -m 'Initial commit'")
