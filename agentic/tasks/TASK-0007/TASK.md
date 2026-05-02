# Task: Normalize agent metadata files to match live registry records

## ID
`TASK-0007`

Use the next available `TASK-####` identifier from the existing set under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`.

## Status
`draft`

When a task is first opened, start at `draft`. Move to `ready` only after explicit approval to begin implementation. Move to `in_progress` only when Builder-Organizer actually begins execution. Use `done` only when the task is actually complete. When a task reaches `done`, clear the task-level `next_actor` in `tasks.yaml` to `null`.

Reopen the same task only if the goal and scope are still the same. Create a new task id for a new slice, a changed goal, a material scope expansion, or independently tracked follow-up work.

## Branch
`feature/task-0007-normalize-agent-metadata`

## Roadmap Reference
Seventh MVP slice after TASK-0001 through TASK-0006.

## Goal
Make the existing `registry/agents/*.yaml` files match the live registry registration model.

## Context
The live registry model now includes explicit metadata/config fields such as:
- `name`
- `version`
- `description`
- `endpoint`
- `capabilities`
- `interaction_mode`
- `runtime_type`
- `system_prompt`
- `input_schema`
- `output_schema`
- `tool_refs`
- `model`
- `limits`

The existing `registry/agents/*.yaml` files still use an older placeholder shape with fields such as `apiVersion`, `kind`, `metadata`, `spec`, `purpose`, `inputs`, `outputs`, `prompt_ref`, `mcp_dependencies`, and `a2a`.

This task should remove that mismatch without changing runtime behavior or loading the YAML files yet.

## Scope
- normalize only the existing three files:
  - `registry/agents/reader-agent.yaml`
  - `registry/agents/math-agent.yaml`
  - `registry/agents/report-writer-agent.yaml`
- align each YAML file with the live `AgentRegistration` shape
- keep values consistent with `orchestrator/run_demo.py`
- keep all three current agents as `runtime_type: packaged-agent`
- remove obsolete placeholder fields from those YAML files
- add one focused test that parses the YAML files and validates them against `AgentRegistration`
- update docs only if a short clarification is needed

Target shape example:

```yaml
name: reader-agent
version: 0.1.0
description: Reads inline CSV text and returns a normalized table artifact.
endpoint: http://reader-agent:8001
capabilities:
  - read.tabular
interaction_mode: callable
runtime_type: packaged-agent
system_prompt: Parse inline CSV into a structured table artifact.
input_schema:
  type: csv_text
  description: Inline CSV text with a header row.
output_schema:
  artifact_type: table
  description: Columns, rows, and metadata with row_count, column_count, and source_format.
tool_refs: []
model: none
limits:
  timeout: 10
  max_steps: 1
```

## Out of Scope
- loading YAML files in the orchestrator
- registry loader endpoint
- automatic filesystem discovery
- package/catalog/marketplace design
- schema framework
- new agents
- runtime behavior changes
- deployment behavior changes
- A2A
- MCP
- auth
- policy/RBAC
- persistence
- UI

## Dependencies / Prerequisites
- TASK-0002 remains the explicit agent configuration baseline.
- TASK-0006 made `runtime_type` explicit in the live registry model.
- Implementation starts only after this draft is explicitly approved and moved to `ready`.

## Constraints
- keep this as metadata normalization only
- do not wire the YAML files into runtime behavior
- do not invent a new file schema beyond matching the live registry model
- do not add more agent files
- keep docs changes minimal

## Blast Radius
`small`

Likely touches only `registry/agents/*.yaml`, one focused test, and task-local workflow artifacts.

## Rollout Class
`local`

## Risks
- accidentally expanding this into config loading
- drifting into catalog/package design
- making the YAML shape more ambitious than the live registry model

## Artifacts To Update
Expected implementation artifacts, once approved:
- `registry/agents/reader-agent.yaml`
- `registry/agents/math-agent.yaml`
- `registry/agents/report-writer-agent.yaml`
- focused YAML validation test
- docs only if needed
- task-local workflow artifacts

Do not update runtime behavior while this task remains in `draft`.

## Verification Plan
Expected verification, once approved:
- `pytest -q`
- parse all three YAML files
- validate each YAML file against `AgentRegistration`
- confirm all three metadata files use `runtime_type: packaged-agent`
- confirm obsolete placeholder fields are removed

Docker Compose verification is not required unless runtime files are touched.

## Slice Readiness Check
- the goal is clear: normalize existing agent YAML metadata to the live registry shape
- the scope is narrow: three YAML files and a focused validation test
- dependencies are known: live registry model from TASK-0006
- branch intent is clear: `feature/task-0007-normalize-agent-metadata`
- worktree intent is clear: `worktrees/agentarium-task-0007-builder-organizer-a`
- rollout class is local
- verification is concrete
- implementation is blocked until explicit approval moves the task to `ready`

## Coordination Notes
Runtime coordination belongs in `state.yaml`, `tasks.yaml`, and task-local handoff files.

This task should make metadata files consistent with the live registry model, not make them executable.

## Open Questions
None currently. The task is intentionally narrow and ready for approval.

## Rollout Notes
Local-only metadata normalization. No production rollout.

## Done When
- all three existing agent YAML files match the live registry record shape
- obsolete placeholder fields are removed
- focused tests validate the YAML files against `AgentRegistration`
- no runtime behavior changes are introduced
- docs remain accurate
