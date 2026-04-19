# Task: Add a third agent to validate a richer 3-agent stack

## ID
`TASK-0003`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`review`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0003-report-writer-agent`

## Roadmap Reference
Third MVP slice after TASK-0001 and TASK-0002.

## Goal
Extend the current MVP from a 2-agent chain to a small 3-agent stack by adding one new agent, most likely a `report-writer-agent`, so the project can validate a more realistic multi-step composition flow.

## Context
TASK-0001 proved:
- agents can be registered
- agents can be discovered by capability
- a simple registry-driven two-agent HTTP flow works

TASK-0002 made agent configuration more explicit and introduced a minimal descriptive interaction-mode concept without changing runtime behavior.

So far the stack has only proven:
- reader-agent -> math-agent

The next slice should test:
- whether a third agent can consume the previous artifact and produce a final presentation/output layer
- whether the registry remains a clean discovery/composition mechanism as the stack grows slightly
- whether the current agent config/metadata model remains usable with one more callable specialist agent
- one more registry-driven handoff
- one more callable specialist agent
- a richer artifact chain

It should not validate or introduce a generic workflow engine.

## Scope
- add one third agent to the runtime stack
- prefer `report-writer-agent` as the new agent
- define the minimal artifact contract for the report-writing step
- update the orchestrator to perform a 3-step registry-driven flow
- update registration payloads/config as needed within the current MVP model
- add focused tests for the new agent and updated flow where appropriate
- update docs/README only as needed to keep the architecture coherent

Expected 3-agent flow:
1. orchestrator registers all agents
2. orchestrator discovers `reader-agent` by capability
3. reader-agent returns table artifact
4. orchestrator discovers `math-agent` by capability
5. math-agent returns analysis artifact
6. orchestrator discovers `report-writer-agent` by capability
7. report-writer-agent returns final report artifact

Preferred capabilities:
- `read.tabular`
- `analyze.basic-math`
- `report.write`

Likely `report-writer-agent` role:
- accept the analysis artifact from `math-agent`
- produce a concise final report artifact
- remain simple and deterministic enough for MVP purposes

Report artifact direction:
- use a small structured `report` artifact
- include `artifact_type`
- include `summary`
- include `sections`
- include `metadata`
- keep the artifact MVP-sized

## Out of Scope
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- OCI packaging
- ranking/selection among multiple agents
- input abstraction
- adding many new agents
- conversational runtime behavior
- generic workflow engine
- marketplace/catalog features
- UI
- general-purpose natural-language generation design

## Dependencies / Prerequisites
- TASK-0001 remains the working two-agent baseline.
- TASK-0002 remains the current explicit agent config baseline.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep the new agent simple
- keep the report writer narrowly scoped to consuming the analysis artifact and producing a final report artifact
- prefer a formatter-style implementation over broad natural-language generation behavior unless there is a strong reason not to
- preserve the current registry-driven architecture
- avoid over-engineering the artifact model
- keep the stack runnable locally with Docker Compose
- keep tests proportionate to the MVP
- do not introduce conversational runtime behavior
- do not add new ecosystem or marketplace concepts

## Blast Radius
`medium`

The likely implementation touches Docker Compose, one new agent service, orchestrator registration/flow, README/docs, and tests. It should not change the registry architecture beyond adding one more registered agent.

## Rollout Class
`local`

## Risks
- the report artifact could become too broad if this turns into general report generation
- the orchestration flow could become over-abstracted before a generic workflow engine is justified
- docs should distinguish what the 3-agent stack validates from what remains unproven

## Artifacts To Update
Expected implementation artifacts, once approved:
- new `agents/report-writer-agent/` service
- `docker-compose.yml`
- `orchestrator/run_demo.py`
- tests for the report writer and any updated flow behavior
- README and/or architecture docs only where needed
- task-local workflow artifacts

Do not update runtime code while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`
- confirm the orchestrator uses registry capability lookup for all three agents
- confirm the final output comes from `report-writer-agent`

## Slice Readiness Check
- the goal is clear: validate a small 3-agent registry-driven stack
- the scope is narrow: one third agent, report artifact contract, orchestrator update, tests, and concise docs
- dependencies are known: TASK-0001 and TASK-0002 baselines
- branch intent is clear: `feature/task-0003-report-writer-agent`
- worktree intent is clear: `worktrees/agentarium-task-0003-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

Implementation completed within the locked report-writer-agent scope and is ready for review.

## Open Questions
Resolved for this slice:
- the report artifact is a small structured `report` artifact with `artifact_type`, `summary`, `sections`, and `metadata`
- the report writer should be deterministic and formatter-style, not broad natural-language generation
- TASK-0003 validates one more registry-driven handoff, one more callable specialist agent, and a richer artifact chain, not a generic workflow engine

Remaining implementation choice:
- which focused test best verifies the updated 3-step flow without adding a broad integration framework?

## Rollout Notes
Local-only MVP slice. No production rollout.

## Done When
- a third agent is registered in the registry
- `report-writer-agent` consumes the math analysis artifact
- `report-writer-agent` produces a final report artifact
- the orchestrator runs a 3-step registry-driven demo flow
- registry capability lookup is used for `read.tabular`, `analyze.basic-math`, and `report.write`
- focused tests cover the new agent and updated behavior at an MVP-appropriate level
- Docker Compose still runs the local stack
- docs remain concise and do not expand into broader workflow-engine or ecosystem design
- no A2A, MCP, auth, policy, persistence, packaging, ranking, marketplace, UI, input-abstraction, or conversational runtime work is added
