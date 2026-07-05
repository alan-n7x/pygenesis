from __future__ import annotations

from pathlib import Path

import yaml

from pygenesis.models.config import ProjectConfig


class ConfigLoader:
    @staticmethod
    def load(path: str | Path) -> ProjectConfig:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        if path.suffix not in {".yaml", ".yml"}:
            raise ValueError(f"Config file must be YAML: {path}")

        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        if not isinstance(data, dict):
            raise ValueError("Config file must contain a YAML mapping")

        return ProjectConfig.from_dict(data)

    @staticmethod
    def generate_default(name: str, owner: str, author_name: str, author_email: str) -> str:
        package = name.replace("-", "_")
        return f"""project:
  name: {name}
  package: {package}
  version: 0.1.0

author:
  name: {author_name}
  email: {author_email}

github:
  owner: {owner}

license: MIT

debian:
  ppa: tools

python:
  minimum: "3.12"
"""
