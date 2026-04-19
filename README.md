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
- small service-level tests

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
- accept inline CSV text
- return a normalized tabular artifact

### `math-agent`
Capability:
- `analyze.basic-math`

Responsibility:
- accept a normalized tabular artifact
- compute safe basic numeric metrics and simple findings

## Registry model

Each agent record contains only the minimum needed for discovery:
- `name`
- `version`
- `endpoint`
- `capabilities`

This keeps the MVP simple while leaving a clean path to richer metadata later.

Registration stores the agent base endpoint URL, not the `/invoke` path.
Capability search returns a list of matching agents.

## Minimal artifact contract

Agent registration:

```json
{
  "name": "reader-agent",
  "version": "0.1.0",
  "endpoint": "http://reader-agent:8001",
  "capabilities": ["read.tabular"]
}
```

Reader output:

```json
{
  "artifact_type": "table",
  "columns": ["region", "sales"],
  "rows": [
    {"region": "A", "sales": 100},
    {"region": "B", "sales": 80}
  ],
  "metadata": {
    "row_count": 2
  }
}
```

Math agent output:

```json
{
  "artifact_type": "analysis",
  "metrics": {
    "row_count": 2,
    "numeric_columns": {
      "sales": {
        "count": 2,
        "sum": 180,
        "average": 90,
        "min": 80,
        "max": 100
      }
    }
  },
  "findings": [
    "Column sales has average 90 across 2 numeric values."
  ]
}
```

## Local run

Start the three long-running services:

```bash
docker compose up --build
```

In another terminal, run the registry-driven demo:

```bash
docker compose run --rm orchestrator
```

The orchestrator registers `reader-agent` and `math-agent`, finds them through registry capability lookup, sends inline CSV to the reader, passes the table artifact to the math agent, and prints the final analysis artifact.

Stop the local stack:

```bash
docker compose down
```

## Tests

Install local test dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
```

Run the service-level tests:

```bash
pytest
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
