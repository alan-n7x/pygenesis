import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pygenesis.generators.project import ProjectGenerator  # noqa: E402
from pygenesis.models.config import (  # noqa: E402
    AuthorConfig,
    GitHubConfig,
    ProjectConfig,
    ProjectMetadata,
)


def _make_config(name: str = "my-app") -> ProjectConfig:
    return ProjectConfig(
        project=ProjectMetadata(name=name, package=name.replace("-", "_"), version="0.1.0"),
        author=AuthorConfig(name="Test", email="test@example.com"),
        github=GitHubConfig(owner="testuser"),
    )


def test_generator_creates_project(tmp_path: Path) -> None:
    config = _make_config()
    generator = ProjectGenerator()
    project_dir = generator.generate(config, tmp_path)

    assert project_dir.is_dir()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "src" / config.module_name).is_dir()
    assert (project_dir / "src" / config.module_name / "__init__.py").exists()
    assert (project_dir / "src" / config.module_name / "cli.py").exists()
    assert (project_dir / "tests").is_dir()
    assert (project_dir / "tests" / "test_cli.py").exists()


def test_generator_creates_debian_files(tmp_path: Path) -> None:
    config = _make_config()
    generator = ProjectGenerator()
    project_dir = generator.generate(config, tmp_path)

    debian_dir = project_dir / "debian"
    assert debian_dir.is_dir()
    assert (debian_dir / "control").exists()
    assert (debian_dir / "rules").exists()
    assert (debian_dir / "copyright").exists()
    assert (debian_dir / "changelog").exists()
    assert (debian_dir / "source" / "options").exists()


def test_generator_creates_github_workflows(tmp_path: Path) -> None:
    config = _make_config()
    generator = ProjectGenerator()
    project_dir = generator.generate(config, tmp_path)

    workflows = project_dir / ".github" / "workflows"
    assert workflows.is_dir()
    assert (workflows / "ci.yml").exists()
    assert (workflows / "release.yml").exists()
    assert (workflows / "launchpad.yml").exists()


def test_generator_renders_variables(tmp_path: Path) -> None:
    config = _make_config("hello-world")
    generator = ProjectGenerator()
    project_dir = generator.generate(config, tmp_path)

    pyproject = project_dir / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    assert 'name = "hello-world"' in content
    assert 'version = "0.1.0"' in content

    init_file = project_dir / "src" / "hello_world" / "__init__.py"
    init_content = init_file.read_text(encoding="utf-8")
    assert '__version__ = "0.1.0"' in init_content
