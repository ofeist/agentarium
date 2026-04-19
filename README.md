# agentarium MVP

agentarium is an open-source agent registry for capability-based discovery and composition.

## What this MVP is

This repository is the **minimum viable prototype** for an agent registry idea.

It does **not** try to solve the full future of agent interoperability.
It proves one small but important thing:

> agents can be registered, discovered by capability, and composed into a tiny workflow through a registry.

## MVP goal

Demonstrate this end-to-end flow:

1. Register two agents in a registry.
2. Search the registry by capability.
3. Invoke the matching agent over HTTP.
4. Pass the output artifact from one agent to another.
5. Produce a final result.

## MVP scope

Included:
- a small registry service
- a `reader-agent`
- a `math-agent`
- a simple orchestrator script
- one sample CSV file
- Docker Compose for local startup

Explicitly excluded for now:
- A2A implementation
- MCP implementation
- auth / RBAC / approvals
- UI
- OCI packaging
- full standardization work
- marketplace features
- advanced observability

## Agents in this MVP

### `reader-agent`
Capability:
- `read.tabular`

Responsibility:
- accept CSV input or a file path
- return a normalized tabular artifact

### `math-agent`
Capability:
- `analyze.basic-math`

Responsibility:
- accept a normalized tabular artifact
- compute a small summary (sum, average, min, max, count)

## Registry model

Each agent record contains only the minimum needed for discovery:
- `name`
- `version`
- `endpoint`
- `capabilities`

This keeps the MVP simple while leaving a clean path to richer metadata later.

## Minimal artifact contract

Reader output:

```json
{
  "artifact_type": "table",
  "data": [
    {"region": "A", "sales": 100},
    {"region": "B", "sales": 80}
  ]
}
```

Math agent output:

```json
{
  "artifact_type": "analysis",
  "result": {
    "count": 2,
    "sum_sales": 180,
    "avg_sales": 90,
    "min_sales": 80,
    "max_sales": 100
  }
}
```

## Why Docker Compose

Docker Compose is used here only as a **local stack runner**.
It is not part of the business logic.

Reasons:
- keeps services isolated
- makes the stack easy to run locally
- matches the mental model of a multi-component agent stack
- can be removed later if it proves unnecessary

## Repository layout

See `docs/REPO_STRUCTURE.md`.

## Suggested next steps after MVP

1. add a third agent (`report-writer-agent`)
2. add persistent storage to the registry
3. add richer metadata (input/output schema, tool requirements)
4. add ranking when multiple agents match the same capability
5. experiment with A2A-compatible metadata
