from __future__ import annotations

from pygenesis.models.config import ProjectConfig


class ConfigValidator:
    ERRORS: list[str] = []

    @classmethod
    def validate(cls, config: ProjectConfig) -> list[str]:
        cls.ERRORS = []
        checks = [
            cls._check_project_name,
            cls._check_project_version,
            cls._check_author_name,
            cls._check_author_email,
            cls._check_github_owner,
            cls._check_python_minimum,
        ]
        for check in checks:
            check(config)
        return cls.ERRORS

    @classmethod
    def _check_project_name(cls, config: ProjectConfig) -> None:
        if not config.project.name or len(config.project.name) < 2:
            cls.ERRORS.append("Project name must have at least 2 characters")

    @classmethod
    def _check_project_version(cls, config: ProjectConfig) -> None:
        import re
        if not re.match(r"^\d+\.\d+\.\d+$", config.project.version):
            cls.ERRORS.append(f"Invalid version: {config.project.version} (expected semver)")

    @classmethod
    def _check_author_name(cls, config: ProjectConfig) -> None:
        if not config.author.name:
            cls.ERRORS.append("Author name is required")

    @classmethod
    def _check_author_email(cls, config: ProjectConfig) -> None:
        if "@" not in config.author.email:
            cls.ERRORS.append(f"Invalid email: {config.author.email}")

    @classmethod
    def _check_github_owner(cls, config: ProjectConfig) -> None:
        if not config.github.owner:
            cls.ERRORS.append("GitHub owner is required")

    @classmethod
    def _check_python_minimum(cls, config: ProjectConfig) -> None:
        import re
        if not re.match(r"^\d+\.\d+$", config.python.minimum):
            cls.ERRORS.append(f"Invalid Python version: {config.python.minimum}")
