# Task: Make runtime type explicit in the live registry

## ID
`TASK-0006`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`done`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0006-runtime-type`

## Roadmap Reference
Sixth MVP slice after TASK-0001 through TASK-0005.

## Goal
Promote `runtime_type` from docs and placeholder agent YAML into the live registry registration model.

The field should make the distinction explicit between:
- agent identity/configuration
- how an agent is executed or packaged

## Context
The repository already mentions `runtime_type` in architecture/docs and placeholder registry agent YAML files.

However, the live registry service does not yet define or validate `runtime_type`, and the orchestrator does not include it in registration payloads.

TASK-0006 should close that gap without adding new runtime behavior.

## Scope
- add `runtime_type` to the live `AgentRegistration` model
- validate allowed `runtime_type` values
- update orchestrator registration payloads for the current three agents
- update focused registry tests
- update README/docs only where needed to align live behavior with current architecture notes
- keep the field descriptive metadata only

Allowed values for this slice:
- `packaged-agent`
- `generic-llm-agent`

Likely current MVP registrations:
- `reader-agent`: `packaged-agent`
- `math-agent`: `packaged-agent`
- `report-writer-agent`: `packaged-agent`

Reason: all three are currently concrete FastAPI services run by Docker Compose.

## Out of Scope
- new runtime behavior
- shared generic LLM runtime
- model invocation
- Docker image metadata
- packaging format
- deployment system
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- ranking/selection
- UI
- marketplace/catalog features

## Dependencies / Prerequisites
- TASK-0002 remains the explicit agent configuration baseline.
- TASK-0003 remains the current 3-agent stack baseline.
- TASK-0004 remains the clarified artifact contract baseline.
- TASK-0005 remains the clarified orchestrator flow baseline.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep `runtime_type` descriptive only
- do not branch runtime behavior based on `runtime_type`
- do not introduce a generic runtime host
- do not redesign agent packaging
- do not expand placeholder YAML into a full registry loader
- keep the patch focused on model, payloads, tests, and concise docs alignment

## Blast Radius
`small`

Likely touches registry model/tests, orchestrator registration payloads, README/docs, and possibly placeholder YAML alignment.

## Rollout Class
`local`

## Risks
- implying support for a generic LLM runtime before one exists
- confusing runtime type with Docker image/package metadata
- drifting into packaging or deployment design

## Artifacts To Update
Expected implementation artifacts, once approved:
- `registry/app.py`
- `orchestrator/run_demo.py`
- `tests/test_registry.py`
- README/docs only where needed
- `registry/agents/*.yaml` only if aligning placeholder metadata is necessary
- task-local workflow artifacts

Do not update runtime code while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest -q`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`
- confirm current agent registrations include `runtime_type`
- confirm invalid `runtime_type` is rejected
- confirm demo behavior is unchanged

## Slice Readiness Check
- the goal is clear: make `runtime_type` live registry metadata
- the scope is narrow: model, payloads, tests, and small docs alignment
- dependencies are known: TASK-0002 through TASK-0005 baselines
- branch intent is clear: `feature/task-0006-runtime-type`
- worktree intent is clear: `worktrees/agentarium-task-0006-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task should make runtime type explicit, not implement runtime selection.

Approved, implemented, reviewed, and merged from `feature/task-0006-runtime-type`.

## Open Questions
Resolved before implementation:
- correct only the `runtime_type` field in `registry/agents/*.yaml` from `generic-llm-agent` to `packaged-agent` for the three current FastAPI services
- do not broaden the YAML cleanup beyond `runtime_type`; the prompt-oriented YAML shape remains out of scope
- make `runtime_type` required in the live registration payload
- reject missing or invalid `runtime_type` through validation
- group `runtime_type` with registry metadata in docs/tests because it describes execution/hosting style, not prompt/config behavior
- keep `runtime_type` descriptive only; validate and echo it, but do not branch runtime behavior on it

Implementation was reviewed, merged, and closed.

## Rollout Notes
Local-only MVP slice. No production rollout.

## Done When
- registry accepts and returns `runtime_type`
- invalid `runtime_type` is rejected
- all current orchestrator registrations include `runtime_type`
- docs explain the field without implying new runtime support
- existing demo behavior is unchanged
- no new runtime host, packaging system, or deployment behavior is introduced
