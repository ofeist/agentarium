# Worktree Policy

## Purpose

Use separate worktrees when parallel work is needed, but keep the first usable workflow simple.

## Rules

- one active branch has one writer at a time
- task ownership must be clear in `tasks.yaml`
- reviewer or QA work should use separate branches or worktrees when they need to make changes
- parallel work is allowed only when write scopes do not overlap
- if overlap exists, keep one side read-only or sequence the work

## Naming Convention

- linked worktrees live under the repo-local `worktrees/` directory
- worktrees use `worktrees/<repo>-<task-id>-<actor-id>`
- branches use `<type>/<task-id>-<slug>`
- allowed task types are `feature`, `fix`, `chore`, and `docs`
- future review or QA branches may use `review/<task-id>-<slug>` or `qa/<task-id>-<slug>` when needed

Actor-aware worktree naming matters because it keeps concurrent task work readable, avoids collisions when more than one agent touches the same task, and makes ownership visible in `tasks.yaml` and local filesystem layout.

## Normal Solo Start

- one task
- one branch
- one worktree
- one `builder-organizer`

## Multi-Agent Expansion

When parallel work is needed:
- assign each active task an owner
- record branch and worktree in `tasks.yaml`
- use task-local handoff files for explicit state changes
- integrate review or QA patches back into the task branch explicitly
