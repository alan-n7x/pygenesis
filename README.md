# PyGenesis

Professional Python project generator — **PyPI**, **APT**, and **Launchpad** ready.

Generate production-ready Python projects that can be published to PyPI, GitHub Releases, and Ubuntu PPAs with zero additional configuration.

## Installation

```bash
pip install pygenesis
```

Or via `uv`:

```bash
uv tool install pygenesis
```

## Quick Start

```bash
pygenesis new my-project
cd my-project
# Edit pygenesis.yaml with your info
pygenesis validate
pygenesis build
```

## Commands

| Command | Description |
|---------|-------------|
| `new` | Generate a new project from a template |
| `init` | Initialize pygenesis.yaml in an existing project |
| `doctor` | Check your system for required tools |
| `release` | Bump version, tag, push, and trigger CI/CD |
| `build` | Build wheel and sdist |
| `publish` | Upload to PyPI |
| `validate` | Validate pygenesis.yaml configuration |

## Usage

```bash
# Generate a Python CLI project
pygenesis new hello-world

# Generate with a custom config
pygenesis new my-app --config my-config.yaml

# Generate using a specific template
pygenesis new my-api --template fastapi

# Validate your config
pygenesis validate pygenesis.yaml

# Check system requirements
pygenesis doctor

# Build distribution packages
pygenesis build

# Full release (bump, tag, push)
pygenesis release --bump minor
```

## Architecture

```
src/pygenesis/
├── cli/              # CLI commands (Typer)
│   └── commands/     # Command implementations
├── config/           # YAML loading and validation
├── generators/       # Project generation logic
├── models/           # Data models (dataclasses)
├── render/           # Jinja2 rendering engine
├── services/         # Release, build, publish services
├── templates/        # Jinja2 templates per project type
│   ├── python-cli/
│   ├── python-daemon/
│   ├── python-library/
│   ├── fastapi/
│   └── streamlit/
└── utils/            # File utilities, template filters
```

## Generated Project Structure

```
my-project/
├── src/my_project/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── debian/
│   ├── control
│   ├── rules
│   ├── copyright
│   ├── changelog
│   ├── install
│   ├── links
│   ├── postinst
│   ├── prerm
│   ├── source/options
│   └── *.service
├── .github/workflows/
│   ├── ci.yml
│   ├── release.yml
│   └── launchpad.yml
├── pyproject.toml
├── Makefile
├── pygenesis.yaml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
└── .pre-commit-config.yaml
```

## CI/CD Pipelines

### CI
Runs on every push/PR: Ruff linting, MyPy type checking, Pytest.

### Release
On tag `v*`: tests, build wheel/sdist, publish to PyPI, create GitHub Release.

### Launchpad
On tag `v*`: build source package, GPG sign, dput to PPA.

## Configuration (pygenesis.yaml)

```yaml
project:
  name: hello-world
  package: hello_world
  version: 0.1.0

author:
  name: Your Name
  email: your@email.com

github:
  owner: your-username

license: MIT

debian:
  ppa: tools

python:
  minimum: "3.12"
```

## Templates

| Template | Type |
|----------|------|
| `python-cli` | Python CLI application with argparse |
| `python-daemon` | Python systemd daemon |
| `python-library` | Python library package |
| `fastapi` | FastAPI web application |
| `streamlit` | Streamlit data app |

## Doctor

```bash
pygenesis doctor
```

Checks for:
- Python 3.12+
- uv
- git
- GPG
- dput
- debhelper
- GitHub CLI (gh)
- PyPI token (~/.pypirc)

## Development Cycle

```
1. pygenesis new meu-app     → gera projeto pronto
2. cd meu-app                → edita pygenesis.yaml
3. pygenesis validate        → valida config
4. code ...                  → implementa funcionalidade
5. pygenesis build           → gera wheel + sdist
6. git add . && git commit
7. pygenesis release         → bump version + tag + push
                              → GitHub Actions:
                                • ruff + mypy + pytest
                                • publica PyPI (pip install)
                                • cria GitHub Release
                                • envia p/ Launchpad → .deb (apt install)
```

### Setup inicial (uma vez)

```bash
pygenesis new meu-app
cd meu-app
# edita pygenesis.yaml com nome, email, github
git init && git add . && git commit -m "init"
git remote add origin git@github.com:seu-user/meu-app.git
git push -u origin main
# configura secrets no GitHub:
#   PYPI_TOKEN, GPG_PRIVATE_KEY, GPG_PASSPHRASE, GPG_KEY_ID
```

### Ciclo diário

```bash
# codifica ...
ruff check src/
mypy src/
pytest
git add . && git commit -m "feat: ..."
git push
```

### Release

```bash
pygenesis release --bump patch   # ou minor, major
# isso faz bump + tag + push → CI/CD automático
```

### Instalação pelos usuários

```bash
pip install meu-app               # PyPI
sudo apt install meu-app          # APT (via PPA)
```

## Requirements

- Python 3.12+
- uv (recommended) or pip

## License

MIT
