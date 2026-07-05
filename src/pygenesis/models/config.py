from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LicenseType(StrEnum):
    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    GPL_3_0 = "GPL-3.0"
    BSD_3_CLAUSE = "BSD-3-Clause"
    MPL_2_0 = "MPL-2.0"
    UNLICENSED = "UNLICENSED"


class TemplateType(StrEnum):
    PYTHON_CLI = "python-cli"
    PYTHON_DAEMON = "python-daemon"
    PYTHON_LIBRARY = "python-library"
    FASTAPI = "fastapi"
    STREAMLIT = "streamlit"


@dataclass
class AuthorConfig:
    name: str
    email: str


@dataclass
class GitHubConfig:
    owner: str


@dataclass
class DebianConfig:
    ppa: str = "tools"


@dataclass
class PythonConfig:
    minimum: str = "3.12"


@dataclass
class ProjectMetadata:
    name: str
    package: str
    version: str


@dataclass
class ProjectConfig:
    project: ProjectMetadata
    author: AuthorConfig
    github: GitHubConfig
    license: LicenseType = LicenseType.MIT
    debian: DebianConfig = field(default_factory=DebianConfig)
    python: PythonConfig = field(default_factory=PythonConfig)
    template: TemplateType = TemplateType.PYTHON_CLI

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectConfig:
        proj = data["project"]
        author = data["author"]
        github = data["github"]

        return cls(
            project=ProjectMetadata(
                name=proj["name"],
                package=proj.get("package", proj["name"].replace("-", "_")),
                version=proj.get("version", "0.1.0"),
            ),
            author=AuthorConfig(
                name=author["name"],
                email=author["email"],
            ),
            github=GitHubConfig(owner=github["owner"]),
            license=LicenseType(data.get("license", "MIT")),
            debian=DebianConfig(ppa=data.get("debian", {}).get("ppa", "tools")),
            python=PythonConfig(minimum=data.get("python", {}).get("minimum", "3.12")),
            template=TemplateType(data.get("template", "python-cli")),
        )

    @property
    def module_name(self) -> str:
        return self.project.package

    @property
    def github_repo(self) -> str:
        return f"{self.github.owner}/{self.project.name}"

    @property
    def github_url(self) -> str:
        return f"https://github.com/{self.github_repo}"

    @property
    def debian_package(self) -> str:
        return self.project.name.replace("_", "-").lower()
