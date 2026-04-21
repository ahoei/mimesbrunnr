# Contributing

Thank you for contributing! Please read this guide before opening a pull request.

---

## Branch Strategy

We follow a structured branching model designed for versioned releases.

```
main          — production-ready code, tagged releases only
develop       — integration branch, all features land here first
feature/*     — new features (e.g. feature/add-auth)
fix/*         — bug fixes (e.g. fix/login-crash)
release/*     — release preparation (e.g. release/v1.0.0)
hotfix/*      — urgent fixes branched directly off main
```

### Flow

```
feature/* ──→ develop ──→ release/* ──→ main (tagged vX.Y.Z)
                                    hotfix/* ──→ main + develop
```

---

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) for dependency management
- [Docker](https://www.docker.com/) / [Podman](https://podman.io/) for the devcontainer
- [Make](https://www.gnu.org/software/make/) for running commands

### Setup

```bash
# Install dependencies and pre-commit hooks
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
| `make bump-patch` | Bump patch version, commit and tag |
| `make bump-minor` | Bump minor version, commit and tag |
| `make bump-major` | Bump major version, commit and tag |

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

All PRs must pass CI before merging. The pipeline runs automatically on every PR and checks:

- Ruff linting
- Ruff format check
- Pytest test suite

PRs that fail CI will not be merged.

---

## Release Process

Releases are managed by maintainers using [`bump-my-version`](https://github.com/callowayproject/bump-my-version) to automate version bumping, committing, and tagging.

### Version scheme

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Bump | When | Command |
|---|---|---|
| `patch` | Bug fixes, small improvements | `make bump-patch` |
| `minor` | New backwards-compatible features | `make bump-minor` |
| `major` | Breaking changes | `make bump-major` |

### Steps

```bash
# 1. Cut a release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z

# 2. Bump the version — updates pyproject.toml, commits, and tags automatically
make bump-patch   # or bump-minor / bump-major

# 3. Push the branch and the tag
git push origin release/vX.Y.Z
git push origin --tags   # triggers the release pipeline on GitHub

# 4. Open a PR: release/vX.Y.Z → main
# 5. After merge, sync develop
git checkout develop
git merge main
git push origin develop
```

Pushing the tag triggers the release pipeline which runs all checks, builds the package, and publishes a GitHub Release automatically.

---

## Branch Protection

Both `main` and `develop` are protected:

- Direct pushes are not allowed
- All changes must come through a Pull Request
- CI must pass before merging
- At least one reviewer approval is required on `main`
