# Contributing

Thank you for contributing! Please read this guide before opening a pull request.

---

## Branch Strategy

We use **GitHub Flow** — a simple, lightweight branching model.

```
main        — production-ready code, always deployable
feature/*   — all work happens here (features, fixes, chores)
```

### Flow

```
feature/your-thing  →  PR + CI  →  main  →  tag (optional release)
```

---

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) for dependency management
- [Docker](https://www.docker.com/) / [Podman](https://podman.io/) for the devcontainer
- [Make](https://www.gnu.org/software/make/) for running commands

### Setup

```bash
make install
```

### Useful commands

| Command | Description |
|---|---|
| `make lint` | Run ruff linter |
| `make format` | Format code with ruff |
| `make fix` | Auto-fix lint issues |
| `make test` | Run tests |
| `make check` | Run all checks (lint + format + tests) |
| `make pre-commit-run` | Run pre-commit hooks on all files |
| `make build` | Build the package |
| `make clean` | Remove build artifacts and caches |
| `make release VERSION=1.2.0` | Tag and push a release |

---

## Making a Contribution

### 1. Branch off main

```bash
git checkout main
git pull origin main
git checkout -b feature/your-thing
```

Use a descriptive branch name that reflects the work: `feature/add-auth`, `fix/login-crash`, `chore/update-deps`.

### 2. Make your changes

Keep commits small and focused. Write clear commit messages:

```
Add user authentication endpoint
Fix null pointer in config loader
Refactor database connection pool
```

### 3. Run checks before pushing

```bash
make check
```

This runs lint, format check, and tests. All must pass before opening a PR.

### 4. Push and open a Pull Request

```bash
git push origin feature/your-thing
```

Open a PR on GitHub targeting **`main`**. Fill in the PR description explaining what changed and why. Get at least one approval and wait for CI to pass before merging.

---

## CI Pipeline

All PRs must pass CI before merging. The pipeline runs automatically on every PR to `main` and checks:

- Ruff linting
- Ruff format check
- Pytest test suite

PRs that fail CI will not be merged.

---

## Release Process

Not every merge to `main` is a release. When you're ready to cut a version:

```bash
make release VERSION=1.2.0
```

This tags `v1.2.0` on `main` and pushes it, which triggers the release pipeline. The pipeline runs all checks, bumps the version in `pyproject.toml`, builds the package, and publishes a GitHub Release with auto-generated release notes.

### Version scheme

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Bump | When |
|---|---|
| `patch` | Bug fixes, small improvements |
| `minor` | New backwards-compatible features |
| `major` | Breaking changes |

---

## Branch Protection

`main` is protected:

- Direct pushes are not allowed
- All changes must come through a Pull Request
- CI must pass before merging
- At least one reviewer approval is required

## Commit Messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/).
Format: `<type>: <description>`
Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`
