---
name: "project-name"
status: planning     # planning | active | paused | done
priority: medium     # low | medium | high
created: YYYY-MM-DD
updated: YYYY-MM-DD
skills:
  - "[[skill-name]]"
tags: [project]
---

# Project: {{Project Name}}

## Goal
One sentence. What does this project accomplish?

## Context
Why does this exist? What problem does it solve?

## Skills Used
List the skills this project relies on, with notes on how each is used.

| Skill | How it's used |
|---|---|
| [[skill-name]] | Brief description |

## Agent Instructions
Specific guidance for agents working on this project.

```
Any persistent instructions, constraints, or preferences the agent should follow
throughout this project. For example: always write code in Python, never modify
files outside /src, prefer brevity in summaries.
```

## File Map
Key files and folders the agent should know about.

```
project-root/
├── src/           # main source code
├── docs/          # documentation
└── outputs/       # agent-generated outputs
```

## Tasks

### Backlog
- [ ] Task description — add any relevant notes

### In Progress
- [ ] Task description

### Done
- [x] Task description — completed YYYY-MM-DD

## Notes & Decisions
Log important decisions and why they were made.

- **YYYY-MM-DD** — Decision: why it was made

## Agent Log
A running record of what agents have done on this project.

- **YYYY-MM-DD** — Agent completed X, output saved to Y
