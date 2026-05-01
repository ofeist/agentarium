# Task: Tighten MVP artifact contracts

## ID
`TASK-0004`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`review`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0004-tighten-artifact-contracts`

## Roadmap Reference
Fourth MVP slice after TASK-0001, TASK-0002, and TASK-0003.

## Goal
Make the current `table`, `analysis`, and `report` artifacts a bit more explicit and consistent, without changing the architecture or introducing a schema framework.

## Context
TASK-0001 established the first working registry-driven MVP.

TASK-0002 made agent configuration more explicit.

TASK-0003 extended the stack to a 3-agent flow:
- `reader-agent` -> `math-agent` -> `report-writer-agent`

The stack works today, but the artifact contracts remain intentionally thin. Before further orchestrator or config work, the current handoff shapes should be tightened slightly so:
- required vs optional fields are clearer
- naming is more consistent across artifacts
- tests and docs describe the current contracts more explicitly

This task should clarify the existing artifact model, not turn it into a generalized protocol or schema system.

## Scope
- review the current artifact shapes used by `reader-agent`, `math-agent`, and `report-writer-agent`
- define slightly clearer MVP contracts for:
  - `table`
  - `analysis`
  - `report`
- make required vs optional fields more explicit
- keep field naming and artifact shape conventions more consistent where practical
- update code, docs, and focused tests to match the clarified contracts
- keep the existing 3-agent demo flow working

Likely contract direction:
- every artifact should keep `artifact_type`
- every artifact should keep `metadata`
- `table` should keep a stable shape around `columns`, `rows`, and `metadata`
- `analysis` should keep a stable shape around `metrics`, `findings`, and `metadata`
- `report` should keep a stable shape around `summary`, `sections`, and `metadata`

## Out of Scope
- JSON Schema framework
- versioned protocol design
- new runtime services
- new agents
- orchestrator redesign
- agent config loading redesign
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- OCI packaging
- ranking/selection
- input abstraction
- conversational runtime behavior
- marketplace/catalog features
- UI

## Dependencies / Prerequisites
- TASK-0001 remains the working MVP baseline.
- TASK-0002 remains the explicit agent configuration baseline.
- TASK-0003 remains the current 3-agent stack baseline.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep the slice small
- clarify current artifact shapes only as much as needed for the existing stack
- avoid a generic schema or standardization exercise
- preserve the current registry-driven architecture
- preserve the current 3-agent flow
- keep tests proportionate to the MVP
- keep docs concise and grounded in implemented behavior

## Blast Radius
`small`

Likely touches agent request/response models, orchestrator assumptions, tests, and concise docs. It should not materially change the runtime architecture.

## Rollout Class
`local`

## Risks
- the slice could drift into over-design if contract clarification becomes a pseudo-standard
- changing artifact shapes too aggressively could break the current demo without meaningful benefit
- docs and tests could get ahead of implementation if the contract language is too abstract

## Artifacts To Update
Expected implementation artifacts, once approved:
- `agents/reader-agent/`
- `agents/math-agent/`
- `agents/report-writer-agent/`
- `orchestrator/run_demo.py` if needed for clarified contracts
- focused tests for current artifact shapes
- README and architecture/docs only where needed
- task-local workflow artifacts

Do not update runtime code while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`
- confirm the existing 3-agent flow still works
- confirm tests and docs match the clarified artifact shapes

## Slice Readiness Check
- the goal is clear: tighten current artifact contracts without widening the architecture
- the scope is narrow: clarify `table`, `analysis`, and `report` artifacts only
- dependencies are known: TASK-0001 through TASK-0003 baselines
- branch intent is clear: `feature/task-0004-tighten-artifact-contracts`
- worktree intent is clear: `worktrees/agentarium-task-0004-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task should stay small and focused on contract clarity, not platform design.

Approved to begin implementation when explicitly started. Approval does not itself start execution.

Implementation was completed on `feature/task-0004-tighten-artifact-contracts`.

## Open Questions
Resolved in implementation:
- all three current artifacts keep `artifact_type` and `metadata`
- `table` metadata now explicitly includes `row_count`, `column_count`, and `source_format`
- `analysis` metadata now explicitly includes `source_artifact_type`, `row_count`, `numeric_column_count`, and `finding_count`
- `report` metadata now explicitly includes `source_artifact_type`, `row_count`, `numeric_column_count`, and `section_count`
- the shared convention is represented both in code models and in concise docs/tests

The slice is implemented and ready for review.

## Rollout Notes
Local-only MVP slice. No production rollout.

## Done When
- current `table`, `analysis`, and `report` artifact contracts are clearer in code and docs
- required vs optional fields are more explicit
- tests reflect the intended shapes
- the 3-agent orchestrator demo still works
- no new services, protocols, or architecture layers are added
- no schema framework or broader standards work is introduced
