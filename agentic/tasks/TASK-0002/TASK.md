# Task: Make agent configuration explicit

## ID
`TASK-0002`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`ready`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0002-agent-configuration`

## Roadmap Reference
Second MVP slice after TASK-0001.

## Goal
Define and prepare the next MVP slice where agent identity and configuration become explicit and structured, instead of agents being described only by `name`, `version`, `endpoint`, and `capabilities`.

## Context
TASK-0001 established the first working MVP:
- agents can be registered
- agents can be discovered by capability
- a simple registry-driven two-agent HTTP flow works

The registry is intentionally thin today. The next slice should move toward a model where an agent is described by endpoint/capabilities and by explicit configuration and interaction shape.

Questions this slice should help answer:
- how does an agent know what it is?
- which parts of agent identity belong in registry metadata vs runtime config?
- which agents are callable vs conversational?
- which fields are important enough to become first-class now?

## Scope
- evolve the agent registration model/schema to include a minimal explicit agent configuration concept
- decide what belongs in registry metadata vs runtime config for the current MVP boundary
- add minimal explicit interaction-mode support
- add or update docs so the architecture stays coherent
- keep the implementation small and focused on config/identity

Intended minimal future agent configuration:
- `name`
- `version`
- `description`
- `system_prompt`
- `capabilities`
- `input_schema`
- `output_schema`
- `tool_refs`
- `model`
- `limits`, for example `timeout` and `max_steps`

For this slice:
- `system_prompt` is stored directly in the registry record
- `input_schema` and `output_schema` are simple descriptive objects, not full JSON Schema
- `model` is a simple string

Registry metadata fields:
- `name`
- `version`
- `description`
- `capabilities`
- `interaction_mode`
- `endpoint`

Agent config fields:
- `system_prompt`
- `input_schema`
- `output_schema`
- `tool_refs`
- `model`
- `limits`

Interaction modes to include:
- `callable`
- `conversational`
- `both`

For TASK-0002, `interaction_mode` is descriptive metadata only. It must not introduce conversational runtime behavior.

Architectural principles to preserve:
- prompt is part of agent configuration
- prompt should not be the whole agent identity
- agent identity/config should become a first-class registry/runtime concept
- not all agents should be conversational
- worker agents are usually callable
- some specialist agents may be conversational
- a manager/front agent may expose conversation while delegating internally

## Out of Scope
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- OCI packaging
- ranking/selection
- input abstraction for filesystem/S3/HTTP
- adding many new agents
- marketplace/catalog features
- UI
- designing a full future standard

## Dependencies / Prerequisites
- TASK-0001 remains the working baseline.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep this as a narrow MVP slice
- do not expand into ecosystem, marketplace, or interoperability design
- keep changes grounded in the current registry/runtime model
- preserve the existing runnable TASK-0001 flow unless a minimal contract update requires a focused adjustment
- avoid premature shared abstraction layers
- distinguish registry metadata from runtime configuration clearly

## Blast Radius
`medium`

The likely implementation touches registry models, orchestrator registration payloads, README/docs, and tests. It should not introduce new runtime services or broad architecture.

## Rollout Class
`local`

## Risks
- the configuration model could become too broad if this turns into standard design work
- adding prompt/config fields without clear boundaries could confuse registry metadata with runtime behavior
- interaction modes should stay descriptive and minimal until more agent types exist

## Artifacts To Update
Expected implementation artifacts, once approved:
- registry registration model/schema
- orchestrator registration payloads
- tests covering richer registration and interaction-mode behavior
- README and/or architecture docs
- task-local workflow artifacts

Do not update runtime code while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`
- review that docs distinguish implemented behavior from intended direction

## Slice Readiness Check
- the goal is clear: make agent configuration explicit as the next MVP concept
- the scope is narrow: registry/config model, interaction mode, docs, and focused tests
- dependencies are known: TASK-0001 runnable MVP baseline
- branch intent is clear: `feature/task-0002-agent-configuration`
- worktree intent is clear: `worktrees/agentarium-task-0002-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task has been approved for implementation. Move to `in_progress` only when execution actually begins.

## Open Questions
Resolved for this slice:
- `system_prompt` is stored directly in the registry record
- `input_schema` and `output_schema` use simple descriptive objects, not full JSON Schema
- `model` is a simple string

## Rollout Notes
Local-only MVP slice. No production rollout.

## Done When
- an explicit richer agent config model is recorded in code and docs
- a minimal interaction-mode concept exists
- registry metadata vs runtime config is clearly distinguished
- the existing registry-driven demo still works
- focused tests cover the new config/interaction-mode behavior
- docs remain concise and do not expand into broader ecosystem design
- no A2A, MCP, auth, policy, persistence, packaging, ranking, marketplace, UI, or input-abstraction work is added
