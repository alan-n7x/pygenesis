import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pygenesis.render.engine import RenderEngine  # noqa: E402


def test_render_engine_renders_string() -> None:
    engine = RenderEngine(ROOT / "src" / "pygenesis" / "templates")
    result = engine.render_string("Hello {{ name }}!", {"name": "World"})
    assert result == "Hello World!"


def test_render_engine_uses_filters() -> None:
    engine = RenderEngine(ROOT / "src" / "pygenesis" / "templates")
    result = engine.render_string(
        "{{ 'hello-world' | snake_case }}",
        {},
    )
    assert result == "hello_world"


def test_render_engine_kebab_filter() -> None:
    engine = RenderEngine(ROOT / "src" / "pygenesis" / "templates")
    result = engine.render_string(
        "{{ 'hello_world' | kebab_case }}",
        {},
    )
    assert result == "hello-world"
