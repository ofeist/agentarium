# Task: Clarify orchestrator composition flow

## ID
`TASK-0005`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`review`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0005-clarify-orchestrator-flow`

## Roadmap Reference
Fifth MVP slice after TASK-0001 through TASK-0004.

## Goal
Clean up the current orchestrator demo so the 3-agent composition is easier to follow and maintain, while preserving the existing MVP architecture and behavior.

## Context
TASK-0001 established the first registry-driven two-agent MVP.

TASK-0002 made agent configuration explicit.

TASK-0003 added `report-writer-agent` and validated a 3-agent flow:
- `reader-agent` -> `math-agent` -> `report-writer-agent`

TASK-0004 tightened the `table`, `analysis`, and `report` artifact contracts.

The next small weak spot is the orchestrator demo. It works, but it manually repeats the same composition pattern:
- register agents
- resolve by capability
- invoke `/invoke`
- pass the returned artifact forward

This task should clarify that flow without turning the orchestrator into a generic workflow engine.

## Scope
- update `orchestrator/run_demo.py`
- keep the current 3-step flow:
  - `read.tabular`
  - `analyze.basic-math`
  - `report.write`
- preserve registry capability lookup for all three agents
- add tiny helper functions only where they reduce repetition and improve readability
- keep registration payloads in the script for this slice
- keep output readable and focused on the final report artifact
- update README/docs only if wording changes are needed
- add or update a small test only if the script becomes testable without awkward mocking

Likely helper direction:
- `resolve_required_agent(capability)`
- `invoke_agent(agent, payload)`
- possibly a small explicit ordered flow in code that still reads like the current demo

## Out of Scope
- generic workflow engine
- DAG or task graph abstraction
- YAML pipeline config
- retry/backoff framework
- ranking or selection among multiple matching agents
- agent config loading redesign
- artifact contract redesign
- new agents
- new runtime services
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- UI
- marketplace/catalog features

## Dependencies / Prerequisites
- TASK-0001 remains the working registry-driven baseline.
- TASK-0002 remains the explicit agent configuration baseline.
- TASK-0003 remains the current 3-agent stack baseline.
- TASK-0004 remains the clarified artifact contract baseline.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep the slice small
- preserve Docker Compose as the local runtime wrapper
- preserve HTTP communication between services
- preserve capability lookup as the composition mechanism
- avoid changing artifact contracts unless a tiny compatibility fix is unavoidable
- do not broaden the orchestrator into product infrastructure
- do not introduce platform concepts beyond the current demo needs

## Blast Radius
`small`

Likely touches only the orchestrator script, maybe concise docs, and possibly one focused test. It should not change service behavior or runtime architecture.

## Rollout Class
`local`

## Risks
- over-abstracting the orchestrator into a premature workflow engine
- hiding capability lookup behind helpers so the demo becomes less explicit
- adding tests that require brittle HTTP mocking instead of keeping the demo simple

## Artifacts To Update
Expected implementation artifacts, once approved:
- `orchestrator/run_demo.py`
- README/docs only if wording changes are needed
- focused test only if it adds value without broad mocking
- task-local workflow artifacts

Do not update runtime code while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`
- confirm all three agents are still resolved through registry capability lookup
- confirm the 3-agent flow still completes and prints the final report artifact

## Slice Readiness Check
- the goal is clear: clarify the current 3-agent orchestrator flow
- the scope is narrow: orchestrator readability and small supporting docs/tests only
- dependencies are known: TASK-0001 through TASK-0004 baselines
- branch intent is clear: `feature/task-0005-clarify-orchestrator-flow`
- worktree intent is clear: `worktrees/agentarium-task-0005-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task should improve clarity of the current demo script, not define a workflow product.

Approved and implemented on `feature/task-0005-clarify-orchestrator-flow`.

## Open Questions
Resolved before implementation:
- keep each orchestration step explicit
- use tiny helpers only for repeated capability resolution and invocation
- skip helper-level unit tests unless implementation introduces meaningful branching
- avoid README changes unless output, commands, or flow wording changes

Implementation is ready for review.

## Rollout Notes
Local-only MVP slice. No production rollout.

## Done When
- the orchestrator code is easier to read and maintain
- the demo behavior remains the same
- registry capability lookup remains explicit for all three agents
- the 3-agent demo flow still completes
- no workflow engine, task graph, pipeline config, or broader orchestration system is introduced
- verification passes or any local environment caveat is recorded clearly
