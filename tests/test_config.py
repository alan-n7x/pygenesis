import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pygenesis.config.loader import ConfigLoader  # noqa: E402
from pygenesis.config.validator import ConfigValidator  # noqa: E402
from pygenesis.models.config import (  # noqa: E402
    AuthorConfig,
    GitHubConfig,
    ProjectConfig,
    ProjectMetadata,
)

SAMPLE_YAML = """project:
  name: hello-world
  package: hello_world
  version: 0.1.0

author:
  name: Alan Santos
  email: alan@example.com

github:
  owner: alan-n7x

license: MIT
"""


def test_config_from_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "pygenesis.yaml"
    config_path.write_text(SAMPLE_YAML, encoding="utf-8")

    config = ConfigLoader.load(config_path)
    assert config.project.name == "hello-world"
    assert config.project.package == "hello_world"
    assert config.project.version == "0.1.0"
    assert config.author.name == "Alan Santos"
    assert config.author.email == "alan@example.com"
    assert config.github.owner == "alan-n7x"
    assert config.module_name == "hello_world"
    assert config.debian_package == "hello-world"


def test_config_validation_passes() -> None:
    config = ProjectConfig(
        project=ProjectMetadata(name="test", package="test", version="0.1.0"),
        author=AuthorConfig(name="Alan", email="alan@test.com"),
        github=GitHubConfig(owner="test"),
    )
    errors = ConfigValidator.validate(config)
    assert errors == []


def test_config_validation_fails() -> None:
    config = ProjectConfig(
        project=ProjectMetadata(name="", package="", version="invalid"),
        author=AuthorConfig(name="", email="bad"),
        github=GitHubConfig(owner=""),
    )
    errors = ConfigValidator.validate(config)
    assert len(errors) > 0


def test_config_from_dict() -> None:
    data = {
        "project": {"name": "my-tool", "package": "my_tool", "version": "1.0.0"},
        "author": {"name": "Author", "email": "a@b.com"},
        "github": {"owner": "user"},
    }
    config = ProjectConfig.from_dict(data)
    assert config.project.name == "my-tool"
    assert config.project.version == "1.0.0"


def test_config_default_template() -> None:
    import yaml
    data = yaml.safe_load(SAMPLE_YAML)
    config = ProjectConfig.from_dict(data)
    assert config.template.value == "python-cli"
