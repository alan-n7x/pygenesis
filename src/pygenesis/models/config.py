from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProjectConfig:
    name: str
    version: str = "0.1.0"


@dataclass
class CIConfig:
    python_versions: list[str] = field(default_factory=lambda: ["3.12"])
    runner: str = "ubuntu-latest"
    lint: bool = True
    type_check: bool = True


@dataclass
class ReleaseConfig:
    branch: str = "main"
    tag_prefix: str = "v"
    changelog: str = "CHANGELOG.md"


@dataclass
class PyPIConfig:
    enabled: bool = True
    environment: str = "pypi"
    trusted_publishing: bool = True


@dataclass
class DebianConfig:
    enabled: bool = True
    email: str = ""
    name: str = ""
    ppa: str = "tools"
    distributions: list[str] = field(default_factory=lambda: ["noble"])
    revision: str = "1"


@dataclass
class PyGenesisConfig:
    project: ProjectConfig
    ci: CIConfig = field(default_factory=CIConfig)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    pypi: PyPIConfig = field(default_factory=PyPIConfig)
    debian: DebianConfig = field(default_factory=DebianConfig)

    @classmethod
    def load(cls, path: str | Path) -> PyGenesisConfig:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")

        raw = path.read_bytes()
        data = tomllib.loads(raw.decode("utf-8"))

        return cls(
            project=ProjectConfig(
                name=data.get("project", {}).get("name", ""),
                version=data.get("project", {}).get("version", "0.1.0"),
            ),
            ci=CIConfig(
                python_versions=data.get("ci", {}).get("python_versions", ["3.12"]),
                runner=data.get("ci", {}).get("runner", "ubuntu-latest"),
                lint=data.get("ci", {}).get("lint", True),
                type_check=data.get("ci", {}).get("type_check", True),
            ),
            release=ReleaseConfig(
                branch=data.get("release", {}).get("branch", "main"),
                tag_prefix=data.get("release", {}).get("tag_prefix", "v"),
                changelog=data.get("release", {}).get("changelog", "CHANGELOG.md"),
            ),
            pypi=PyPIConfig(
                enabled=data.get("pypi", {}).get("enabled", True),
                environment=data.get("pypi", {}).get("environment", "pypi"),
                trusted_publishing=data.get("pypi", {}).get("trusted_publishing", True),
            ),
            debian=DebianConfig(
                enabled=data.get("debian", {}).get("enabled", True),
                email=data.get("debian", {}).get("email", ""),
                name=data.get("debian", {}).get("name", ""),
                ppa=data.get("debian", {}).get("ppa", "tools"),
                distributions=data.get("debian", {}).get("distributions", ["noble"]),
                revision=data.get("debian", {}).get("revision", "1"),
            ),
        )

    @classmethod
    def generate_default(cls, name: str) -> str:
        return f"""[project]
name = "{name}"
version = "0.1.0"

[ci]
python_versions = ["3.12", "3.13"]
runner = "ubuntu-latest"
lint = true
type_check = true

[release]
branch = "main"
tag_prefix = "v"
changelog = "CHANGELOG.md"

[pypi]
enabled = true
environment = "pypi"
trusted_publishing = true

[debian]
enabled = true
email = ""
name = ""
ppa = "tools"
distributions = ["noble"]
revision = "1"
"""

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(self._to_toml(), encoding="utf-8")

    def _to_toml(self) -> str:
        return f"""[project]
name = "{self.project.name}"
version = "{self.project.version}"

[ci]
python_versions = {self.ci.python_versions}
runner = "{self.ci.runner}"
lint = {str(self.ci.lint).lower()}
type_check = {str(self.ci.type_check).lower()}

[release]
branch = "{self.release.branch}"
tag_prefix = "{self.release.tag_prefix}"
changelog = "{self.release.changelog}"

[pypi]
enabled = {str(self.pypi.enabled).lower()}
environment = "{self.pypi.environment}"
trusted_publishing = {str(self.pypi.trusted_publishing).lower()}

[debian]
enabled = {str(self.debian.enabled).lower()}
email = "{self.debian.email}"
name = "{self.debian.name}"
ppa = "{self.debian.ppa}"
distributions = {self.debian.distributions}
revision = "{self.debian.revision}"
"""
