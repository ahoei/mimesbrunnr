# Contributing

Thank you for contributing! Please read this guide before opening a pull request.

---

## Branch Strategy

We follow a structured branching model designed for versioned releases.

```
main          — production-ready code, tagged releases only
develop       — integration branch, all features land here first
feature/*     — new features        (e.g. feature/add-auth)
fix/*         — bug fixes           (e.g. fix/login-crash)
release/*     — release preparation (e.g. release/v1.1.0)
hotfix/*      — urgent fixes branched directly off main
```

### Flow

```
feature/* ──→ develop ──→ release/* ──→ main ──→ tag vX.Y.Z ──→ release pipeline
                                    hotfix/* ──→ main + PR back to develop
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
| `make release VERSION=1.1.0` | Tag and push a release |

---

## Making a Contribution

### 1. Branch off develop

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

Use the appropriate prefix: `feature/`, `fix/`, or `hotfix/`.

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
git push origin feature/your-feature-name
```

Open a PR on GitHub targeting **`develop`** (never directly to `main`). Fill in the PR description explaining what changed and why.

---

## CI Pipeline

All PRs must pass CI before merging. The pipeline runs automatically on every PR to `develop` and `main`, and checks:

- Ruff linting
- Ruff format check
- Pytest test suite

PRs that fail CI will not be merged.

---

## Release Process

Releases are managed by maintainers.

### Version scheme

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Bump | When |
|---|---|
| `patch` | Bug fixes, small improvements |
| `minor` | New backwards-compatible features |
| `major` | Breaking changes |

### Steps

```bash
# 1. Cut a release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# 2. Push and open a PR: release/v1.1.0 → main
git push origin release/v1.1.0
# Open PR on GitHub, wait for CI to pass, get approval, merge

# 3. Tag the release from main
git checkout main
git pull origin main
make release VERSION=1.1.0
# This tags v1.1.0 and pushes it — triggering the release pipeline

# 4. Open a PR: main → develop to keep them in sync
# Do this on GitHub: base: develop ← compare: main
# Title: chore: sync develop with main after v1.1.0
```

The release pipeline automatically bumps the version in `pyproject.toml`, builds the package, and publishes a GitHub Release with auto-generated release notes.

### Hotfixes

For urgent production fixes:

```bash
# Branch off main, not develop
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix

# Fix, commit, push, open PR → main
# After merge, tag a patch release
make release VERSION=1.1.1

# Open a PR: main → develop to bring the fix back
```

---

## Branch Protection

Both `main` and `develop` are protected:

- Direct pushes are not allowed
- All changes must come through a Pull Request
- CI must pass before merging
- At least one reviewer approval is required on `main`
