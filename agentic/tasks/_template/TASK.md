# Task: <title>

## ID
`TASK-####`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`draft` | `ready` | `in_progress` | `review` | `qa` | `blocked` | `done`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`<type>/<task-id>-<slug>`

## Roadmap Reference
Optional:
- iteration / thin-slice reference
- issue / PR link

## Goal
What should be achieved?

## Context
Why are we doing this?
What already exists?

## Scope
What is included in this slice?

## Out of Scope
What must not be touched in this slice?

## Dependencies / Prerequisites
What must already exist or be merged first?

## Constraints
Examples:
- minimal diff
- preserve API shape
- no schema redesign

## Blast Radius
`small` | `medium` | `large`

## Rollout Class
`local` | `ci-local` | `staging` | `prod-sensitive`

## Risks
Known risks or design concerns.

## Artifacts To Update
Which code, docs, config, or workflows are expected to change?

## Verification Plan
Which tests / commands / checks should be run?

## Slice Readiness Check
A task should usually move from `draft` to `ready` only if:
- the goal is clear
- the scope is narrow
- dependencies are known
- branch and worktree intent are clear
- rollout class is chosen when relevant
- verification is concrete
- open questions are either resolved or explicitly accepted

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

## Open Questions
Only if relevant while shaping the task.

## Rollout Notes
Only if relevant.

## Done When
Concrete acceptance criteria.
