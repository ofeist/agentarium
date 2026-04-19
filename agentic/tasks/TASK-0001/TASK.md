# Task: Build first working MVP

## ID
`TASK-0001`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`ready`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0001-working-mvp`

## Roadmap Reference
First MVP slice for `agentarium`.

## Goal
Build the first runnable MVP that proves one thing: agents can be registered, discovered by capability, and invoked through a simple two-agent HTTP flow.

## Context
`agentarium` currently has a minimal scaffold for:
- registry service
- reader-agent service
- math-agent service
- orchestrator demo script
- Docker Compose setup

The current scaffold needs to become actually runnable while staying deliberately small.

## Scope
- real runnable FastAPI services
- in-memory registry
- FastAPI + Pydantic validation
- simple explicit JSON contracts
- HTTP communication between orchestrator and services
- Docker Compose for local development
- reader-agent accepts inline CSV only
- math-agent computes safe basic numeric metrics and simple findings
- small service-level tests only
- README local run instructions

Locked details:
- registry search returns a list of matching agents, even if only one exists today
- agent registration stores the base endpoint URL, not the `/invoke` path
- reader-agent accepts inline CSV only in this first MVP
- math-agent computes only safe basic numeric metrics and simple findings

## Out of Scope
- auth
- UI
- persistent database
- database migrations
- A2A
- MCP
- advanced policy features
- generic plugin system
- service ranking
- async queues
- broad integration test framework
- premature shared abstraction layers

## Dependencies / Prerequisites
- Python service dependencies remain minimal.
- Docker Compose is available for local stack execution.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep the MVP focused on registry-driven discovery plus a working two-agent HTTP flow
- do not over-engineer
- do not add unnecessary frameworks
- keep code clean and easy to extend later
- preserve the existing project name `agentarium`
- use Compose service names for service-to-service communication

## Blast Radius
`medium`

The task touches all MVP runtime components, but the repository is still early and intentionally small.

## Rollout Class
`local`

## Risks
- Docker Compose networking or one-shot orchestrator behavior may need small adjustments.
- CSV parsing should remain simple but must avoid unsafe assumptions about numeric values.
- Service-level tests may not catch all Compose integration failures.

## Artifacts To Update
- `registry/`
- `agents/reader-agent/`
- `agents/math-agent/`
- `orchestrator/`
- `docker-compose.yml`
- `README.md`
- test files needed for the three service-level checks
- dependency files only where needed

## Verification Plan
- `pytest`
- `docker compose up --build` starts `registry`, `reader-agent`, and `math-agent`
- `docker compose run --rm orchestrator` completes the demo flow
- manual or scripted checks that the orchestrator uses registry capability lookup instead of hardcoded agent routing

## Slice Readiness Check
- the goal is clear: one registry-driven two-agent MVP flow
- the scope is narrow: registry, reader-agent, math-agent, orchestrator, Compose, README, service-level tests
- dependencies are known: FastAPI, Pydantic, pytest, an HTTP client, Docker Compose
- branch intent is clear: `feature/task-0001-working-mvp`
- worktree intent is clear: `worktrees/agentarium-task-0001-builder-organizer-a`
- rollout class is local
- verification is concrete
- open questions are resolved or explicitly accepted

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task has been approved for implementation. Move to `in_progress` only when execution actually begins.

## Open Questions
None.

## Rollout Notes
Local-only MVP. No production rollout.

## Done When
- `docker compose up --build` starts `registry`, `reader-agent`, and `math-agent`
- services are reachable
- `docker compose run --rm orchestrator` completes the demo flow
- orchestrator uses registry capability lookup instead of hardcoded agent routing
- reader-agent output is accepted by math-agent
- `pytest` passes for registry, reader-agent, and math-agent core behavior
- README contains exact local run instructions
- any remaining stubs or intentional simplifications are documented
