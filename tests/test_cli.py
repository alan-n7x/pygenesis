import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from typer.testing import CliRunner  # noqa: E402

from pygenesis.cli.app import cli  # noqa: E402

runner = CliRunner()


def test_help_output() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pygenesis" in result.stdout


def test_version_output() -> None:
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout.replace("PyGenesis v", "")


def test_doctor_runs() -> None:
    result = runner.invoke(cli, ["doctor"])
    assert result.exit_code in (0, 1)
    assert "PyGenesis" in result.stdout


def test_new_requires_name() -> None:
    result = runner.invoke(cli, ["new"])
    assert result.exit_code != 0


def test_validate_missing_config(tmp_path: Path) -> None:
    result = runner.invoke(cli, ["validate", str(tmp_path / "nonexistent.yaml")])
    assert result.exit_code == 1
    assert "not found" in result.stdout
