# Contributing

Thanks for taking the time to contribute! This document explains how to get set up, our conventions, and how to submit changes.

---

## Getting started

This project uses a devcontainer to give everyone the same development environment. You need:

- [VS Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Podman](https://podman.io/) (or Docker)

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
code .
```

Then in VS Code: **Command Palette → "Dev Containers: Reopen in Container"**

Dependencies are installed automatically via `uv sync` when the container starts.

---

## Day-to-day workflow

All commands are run inside the devcontainer terminal.

```bash
# Install / sync dependencies
uv sync

# Add a new dependency
uv add <package>

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

Code is auto-formatted on save in VS Code via the Ruff extension.

---

## Branch conventions

Branch off `main` using one of these prefixes:

| Prefix | Use for |
|--------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance, deps, config |
| `docs/` | Documentation only |
| `refactor/` | Code changes with no behaviour change |

Example: `feat/add-parquet-output`

---

## Commit messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add parquet output format
fix: handle empty dataframe in transform
chore: update uv.lock
docs: add usage examples to README
```

Keep the subject line under 72 characters. Add a body if the change needs more context.

---

## Before opening a pull request

Make sure these all pass:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

A CI pipeline will run the same checks on your PR — it's easier to catch issues locally first.

---

## Pull request process

1. Open a PR against `main` with a clear title and description
2. Link any related issues
3. A maintainer will review within a few days
4. Address any feedback, then request a re-review
5. Once approved, the maintainer merges

Keep PRs focused — one concern per PR makes reviewing much easier.

---

## Reporting issues

Open an issue and include:

- What you expected to happen
- What actually happened
- Steps to reproduce
- Python version and OS (if relevant)

---

## Code style

Ruff handles everything — formatting, import sorting, and linting. There's no manual style guide to follow beyond what Ruff enforces. Configuration lives in `pyproject.toml` under `[tool.ruff]`.
