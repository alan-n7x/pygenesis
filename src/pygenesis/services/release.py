from __future__ import annotations

import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pygenesis.models.config import ProjectConfig


class ReleaseService:
    def __init__(self, config: ProjectConfig, project_dir: str | Path | None = None) -> None:
        self.config = config
        self.project_dir = Path(project_dir or Path.cwd()).resolve()

    def dry_run(self, bump: str = "patch") -> None:
        current = self.config.project.version
        next_ver = self._bump_version(current, bump)
        print(f"[DRY RUN] Current version: {current}")
        print(f"[DRY RUN] Next version:    {next_ver}")
        print(f"[DRY RUN] Tag:             v{next_ver}")
        print("[DRY RUN] Would run:")
        print("  1. Update version in pygenesis.yaml")
        print("  2. Update debian/changelog")
        print(f"  3. git add . && git commit -m 'release v{next_ver}'")
        print(f"  4. git tag v{next_ver}")
        print("  5. git push origin main --tags")

    def run(self, bump: str = "patch") -> dict[str, Any]:
        current = self.config.project.version
        next_ver = self._bump_version(current, bump)
        tag = f"v{next_ver}"

        self._update_yaml_version(next_ver)
        self._update_changelog(next_ver)
        self._update_init_version(next_ver)
        self._commit_and_tag(tag)
        self._push()

        return {"version": next_ver, "tag": tag, "pushed": True}

    def _bump_version(self, version: str, bump: str) -> str:
        major, minor, patch = map(int, version.split("."))
        if bump == "major":
            major += 1
            minor = patch = 0
        elif bump == "minor":
            minor += 1
            patch = 0
        else:
            patch += 1
        return f"{major}.{minor}.{patch}"

    def _update_yaml_version(self, new_version: str) -> None:
        yaml_path = self.project_dir / "pygenesis.yaml"
        if not yaml_path.exists():
            return
        content = yaml_path.read_text(encoding="utf-8")
        content = re.sub(
            r"^version:\s*\S+",
            f"version: {new_version}",
            content,
            flags=re.MULTILINE,
        )
        yaml_path.write_text(content, encoding="utf-8")

    def _update_init_version(self, new_version: str) -> None:
        init_path = (
            self.project_dir
            / "src"
            / self.config.module_name
            / "__init__.py"
        )
        if not init_path.exists():
            return
        content = init_path.read_text(encoding="utf-8")
        content = re.sub(
            r'__version__\s*=\s*"[^"]*"',
            f'__version__ = "{new_version}"',
            content,
        )
        init_path.write_text(content, encoding="utf-8")

    def _update_changelog(self, new_version: str) -> None:
        changelog_path = self.project_dir / "CHANGELOG.md"
        if not changelog_path.exists():
            return
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        content = changelog_path.read_text(encoding="utf-8")
        header = f"## [{new_version}] - {today}"
        replacement = f"## [Unreleased]\n\n### Added\n\n### Changed\n\n{header}"
        content = re.sub(r"## \[Unreleased\].*", replacement, content, count=1)
        changelog_path.write_text(content, encoding="utf-8")

    def _commit_and_tag(self, tag: str) -> None:
        subprocess.run(["git", "add", "."], cwd=self.project_dir, check=True, timeout=30)
        subprocess.run(
            ["git", "commit", "-m", f"release {tag}"],
            cwd=self.project_dir,
            check=True,
            timeout=30,
        )
        subprocess.run(
            ["git", "tag", tag],
            cwd=self.project_dir,
            check=True,
            timeout=30,
        )

    def _push(self) -> None:
        subprocess.run(
            ["git", "push", "origin", "main", "--tags"],
            cwd=self.project_dir,
            check=True,
            timeout=60,
        )
