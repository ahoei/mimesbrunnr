# ---------------------------------------------------------------------------
# Project Makefile
# Usage: make <target>
# ---------------------------------------------------------------------------
.DEFAULT_GOAL := help
SHELL         := /bin/bash
PYTHON        := uv run

# ── Help ───────────────────────────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
        | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ── Python / Package ───────────────────────────────────────────────────────
.PHONY: install
install: ## Install all dependencies (including dev) and set up pre-commit hooks
	uv sync --all-extras
	uv run pre-commit install

.PHONY: lint
lint: ## Run ruff linter
	$(PYTHON) ruff check src tests

.PHONY: format
format: ## Format code with ruff
	$(PYTHON) ruff format src tests

.PHONY: format-check
format-check: ## Check formatting without making changes
	$(PYTHON) ruff format --check src tests

.PHONY: fix
fix: ## Auto-fix lint issues with ruff
	$(PYTHON) ruff check --fix src tests

.PHONY: test
test: ## Run tests with pytest
	$(PYTHON) pytest

.PHONY: test-ci
test-ci: ## Run tests in CI mode (no coverage terminal output)
	$(PYTHON) pytest --cov-report=xml

.PHONY: build
build: ## Build the Python package
	uv build

.PHONY: check
check: lint format-check test ## Run all checks (lint + format + tests) — run before pushing

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## Run pre-commit hooks against all files
	$(PYTHON) pre-commit run --all-files

# ── Release ────────────────────────────────────────────────────────────────
.PHONY: release
release: ## Tag and push a release. Usage: make release VERSION=1.1.0
	@test -n "$(VERSION)" || (echo "ERROR: VERSION is required. Usage: make release VERSION=1.1.0" && exit 1)
	git checkout main
	git pull origin main
	git tag v$(VERSION)
	git push origin v$(VERSION)

# ── Clean ──────────────────────────────────────────────────────────────────
.PHONY: clean
clean: ## Remove build artifacts and cache files
	rm -rf dist/ .coverage coverage.xml htmlcov/ .pytest_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
