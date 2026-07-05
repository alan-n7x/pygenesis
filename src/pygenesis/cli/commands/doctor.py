from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from typing import Any

import typer

from pygenesis import __version__


class DoctorCheck:
    def __init__(self, name: str, check_fn: Callable[[], Any], hint: str = "") -> None:
        self.name = name
        self.check_fn = check_fn
        self.hint = hint

    def run(self) -> dict[str, Any]:
        try:
            result = self.check_fn()
            return {"name": self.name, "ok": True, "detail": result, "hint": ""}
        except Exception as exc:
            return {"name": self.name, "ok": False, "detail": str(exc), "hint": self.hint}


def _check_python() -> str:
    return sys.version.split()[0]


def _check_uv() -> str:
    result = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=10)
    return result.stdout.strip()


def _check_git() -> str:
    result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
    return result.stdout.strip()


def _check_gpg() -> str:
    result = subprocess.run(["gpg", "--version"], capture_output=True, text=True, timeout=10)
    first_line = result.stdout.split("\n")[0] if result.stdout else ""
    return first_line


def _check_dput() -> str | None:
    if shutil.which("dput"):
        return "found"
    return None


def _check_debhelper() -> str | None:
    if shutil.which("dh"):
        return "found"
    return None


def _check_gh() -> str | None:
    if shutil.which("gh"):
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True, timeout=10)
        return result.stdout.split("\n")[0] if result.stdout else "found"
    return None


def _check_pypirc() -> str:
    from pathlib import Path
    pypirc = Path.home() / ".pypirc"
    return "found" if pypirc.exists() else "not found"


def doctor_cmd() -> None:
    checks = [
        DoctorCheck("Python", _check_python, "Install Python 3.12+ from python.org"),
        DoctorCheck("uv", _check_uv, "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"),
        DoctorCheck("Git", _check_git, "Install git: apt install git"),
        DoctorCheck("GPG", _check_gpg, "Install gnupg: apt install gnupg"),
        DoctorCheck("dput", _check_dput, "Install dput: apt install dput"),
        DoctorCheck("debhelper", _check_debhelper, "Install debhelper: apt install debhelper"),
        DoctorCheck("GitHub CLI", _check_gh, "Install gh: https://cli.github.com"),
        DoctorCheck(
            "PyPI token (~/.pypirc)", _check_pypirc, "Create ~/.pypirc with your PyPI token"
        ),
    ]

    typer.echo(f"PyGenesis v{__version__} — Doctor")
    typer.echo("")

    all_ok = True
    for check in checks:
        result = check.run()
        if result["ok"]:
            typer.echo(f"  ✓ {result['name']}: {result['detail']}")
        else:
            all_ok = False
            detail = f" ({result['detail']})" if result["detail"] else ""
            typer.echo(f"  ✗ {result['name']}: not found{detail}")
            if result["hint"]:
                typer.echo(f"    → {result['hint']}")

    typer.echo("")
    if all_ok:
        typer.echo("All checks passed!")
    else:
        typer.echo("Some checks failed. Fix the issues above and re-run.")
        raise typer.Exit(code=1)
