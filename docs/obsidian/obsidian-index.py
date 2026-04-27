#!/usr/bin/env python3
"""
obsidian-index.py
Scans an Obsidian vault and regenerates workspace-index.md automatically.

Vault root is expected at: docs/obsidian/ inside your repo.

Usage:
    python docs/obsidian/obsidian-index.py docs/obsidian
    python docs/obsidian/obsidian-index.py docs/obsidian --output custom-index.md
    python docs/obsidian/obsidian-index.py docs/obsidian --dry-run

Set up as a cron job or pre-commit hook to keep the index current.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

SKILLS_DIR = "skills"
PROJECTS_DIR = "projects"
PROMPTS_DIR = "prompts"
OUTPUT_FILE = "meta/workspace-index.md"

STATUS_EMOJI = {
	"stable": "🟢",
	"draft": "🟡",
	"deprecated": "🔴",
	"active": "🟢",
	"planning": "🔵",
	"paused": "🟡",
	"done": "⚫",
}

PRIORITY_EMOJI = {
	"high": "🔴",
	"medium": "🟡",
	"low": "🟢",
}


# ── Frontmatter parser ────────────────────────────────────────────────────────


def parse_frontmatter(text: str) -> dict:
	"""Extract YAML-ish frontmatter from a markdown file. Lightweight — no deps."""
	fm = {}
	if not text.startswith("---"):
		return fm
	end = text.find("---", 3)
	if end == -1:
		return fm
	block = text[3:end].strip()
	for line in block.splitlines():
		if ":" not in line or line.startswith(" ") or line.startswith("-"):
			continue
		key, _, val = line.partition(":")
		fm[key.strip()] = val.strip().strip('"').strip("'")
	return fm


def read_md_files(vault: Path, subdir: str) -> list[dict]:
	"""Return a list of dicts with frontmatter + name + path for all .md files in subdir."""
	folder = vault / subdir
	if not folder.exists():
		return []
	results = []
	for f in sorted(folder.glob("*.md")):
		if f.name.startswith("_"):
			continue
		text = f.read_text(encoding="utf-8")
		fm = parse_frontmatter(text)
		fm.setdefault("name", f.stem)
		fm["_path"] = f.relative_to(vault)
		results.append(fm)
	return results


# ── Section builders ──────────────────────────────────────────────────────────


def build_skills_section(skills: list[dict]) -> str:
	if not skills:
		return "_No skills found in `skills/` — add your first skill card!_\n"

	by_category: dict[str, list] = {}
	for s in skills:
		cat = s.get("category", "uncategorised").split("|")[0].strip()
		by_category.setdefault(cat, []).append(s)

	lines = []
	for cat in sorted(by_category):
		lines.append(f"### {cat.title()}\n")
		lines.append("| Skill | Status | Tags |")
		lines.append("|---|---|---|")
		for s in by_category[cat]:
			status = s.get("status", "draft")
			emoji = STATUS_EMOJI.get(status, "⚪")
			name = s.get("name", s["_path"].stem)
			tags = s.get("tags", "")
			link = f"[[{s['_path'].stem}|{name}]]"
			lines.append(f"| {link} | {emoji} {status} | {tags} |")
		lines.append("")
	return "\n".join(lines)


def build_projects_section(projects: list[dict]) -> str:
	if not projects:
		return "_No projects found in `projects/` — create your first project!_\n"

	active = [p for p in projects if p.get("status") == "active"]
	planning = [p for p in projects if p.get("status") == "planning"]
	other = [
		p for p in projects if p.get("status") not in ("active", "planning", "done")
	]
	done = [p for p in projects if p.get("status") == "done"]

	def table(items):
		if not items:
			return "_None_\n"
		rows = ["| Project | Priority | Skills |", "|---|---|---|"]
		for p in items:
			name = p.get("name", p["_path"].stem)
			priority = p.get("priority", "—")
			p_emoji = PRIORITY_EMOJI.get(priority, "")
			skills = p.get("skills", "")
			link = f"[[{p['_path'].stem}|{name}]]"
			rows.append(f"| {link} | {p_emoji} {priority} | {skills} |")
		return "\n".join(rows) + "\n"

	lines = [
		"### 🟢 Active\n",
		table(active),
		"### 🔵 Planning\n",
		table(planning),
	]
	if other:
		lines += ["### ⚪ Other\n", table(other)]
	lines += ["### ⚫ Done\n", table(done)]
	return "\n".join(lines)


def build_prompts_section(vault: Path) -> str:
	folder = vault / PROMPTS_DIR
	if not folder.exists():
		return "_No prompts directory found — create `prompts/` to start building your library._\n"

	lines = []
	for subfolder in sorted(folder.iterdir()):
		if not subfolder.is_dir():
			continue
		files = sorted(subfolder.glob("*.md"))
		if not files:
			continue
		lines.append(f"**{subfolder.name}/**")
		for f in files:
			lines.append(f"  - [[{f.stem}]]")
	return "\n".join(lines) + "\n" if lines else "_No prompt files found._\n"


# ── Main ──────────────────────────────────────────────────────────────────────


def generate_index(vault: Path) -> str:
	skills = read_md_files(vault, SKILLS_DIR)
	projects = read_md_files(vault, PROJECTS_DIR)

	skill_count = len(skills)
	project_count = len(projects)
	active_count = sum(1 for p in projects if p.get("status") == "active")
	stable_count = sum(1 for s in skills if s.get("status") == "stable")
	now = datetime.now().strftime("%Y-%m-%d %H:%M")

	index = f"""---
auto_generated: true
updated: {now}
tags: [meta, index]
---

# 🗂️ Workspace Index

> Auto-generated by `obsidian-index.py` on {now}.
> Edit skills and projects in their own files — don't edit this file directly.

## 📊 At a Glance

| | Count |
|---|---|
| Skills (total) | {skill_count} |
| Skills (stable) | {stable_count} |
| Projects (total) | {project_count} |
| Projects (active) | {active_count} |

---

## 🔧 Skills

{build_skills_section(skills)}
---

## 📁 Projects

{build_projects_section(projects)}
---

## 💬 Prompts

{build_prompts_section(vault)}
---

## 🤖 Agent Guidelines

See [[agent-guidelines]] for rules and constraints that apply across all agents and projects.

> Vault root: `docs/obsidian/` — open this folder as your Obsidian vault, not the repo root.
"""
	return index


def main():
	parser = argparse.ArgumentParser(
		description="Generate workspace-index.md for your Obsidian agent vault."
	)
	parser.add_argument("vault", help="Path to your Obsidian vault root")
	parser.add_argument(
		"--output",
		default=OUTPUT_FILE,
		help=f"Output path relative to vault (default: {OUTPUT_FILE})",
	)
	parser.add_argument(
		"--dry-run", action="store_true", help="Print output without writing the file"
	)
	args = parser.parse_args()

	vault = Path(args.vault).expanduser().resolve()
	if not vault.exists():
		print(f"Error: vault path not found: {vault}", file=sys.stderr)
		sys.exit(1)

	index_content = generate_index(vault)

	if args.dry_run:
		print(index_content)
		return

	output_path = vault / args.output
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(index_content, encoding="utf-8")
	print(f"✅ Index written to: {output_path}")

	# Summary
	skills = read_md_files(vault, SKILLS_DIR)
	projects = read_md_files(vault, PROJECTS_DIR)
	print(f"   {len(skills)} skills · {len(projects)} projects")


if __name__ == "__main__":
	main()
