from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pygenesis.models.config import TemplateType


@dataclass
class TemplateFile:
    source: Path
    destination: str
    mode: str = "file"


@dataclass
class Template:
    type: TemplateType
    name: str
    description: str
    files: list[TemplateFile] = field(default_factory=list)
    variables: dict[str, Any] = field(default_factory=dict)
