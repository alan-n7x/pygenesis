from __future__ import annotations

import typer

from pygenesis import __version__
from pygenesis.cli.commands.build import build_cmd
from pygenesis.cli.commands.doctor import doctor_cmd
from pygenesis.cli.commands.init import init_cmd
from pygenesis.cli.commands.new import new_cmd
from pygenesis.cli.commands.publish import publish_cmd
from pygenesis.cli.commands.release import release_cmd
from pygenesis.cli.commands.validate import validate_cmd

cli = typer.Typer(
    name="pygenesis",
    help="Professional Python project generator — PyPI, APT, and Launchpad ready",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"PyGenesis v{__version__}")
        raise typer.Exit()


@cli.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    pass


cli.command(name="new")(new_cmd)
cli.command(name="init")(init_cmd)
cli.command(name="doctor")(doctor_cmd)
cli.command(name="release")(release_cmd)
cli.command(name="build")(build_cmd)
cli.command(name="publish")(publish_cmd)
cli.command(name="validate")(validate_cmd)
