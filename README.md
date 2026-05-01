# agentarium MVP

agentarium is an open-source agent registry for capability-based discovery and composition.

## What this MVP is

This repository is the **minimum viable prototype** for an agent registry idea.

It does **not** try to solve the full future of agent interoperability.
It proves one small but important thing:

> agents can be registered, discovered by capability, and composed into a tiny workflow through a registry.

## MVP goal

Demonstrate this end-to-end flow:

1. Register three agents in a registry.
2. Search the registry by capability.
3. Invoke the matching agent over HTTP.
4. Pass output artifacts from one agent to the next.
5. Produce a final report artifact.

## MVP scope

Included:
- a small registry service
- a `reader-agent`
- a `math-agent`
- a `report-writer-agent`
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

### `report-writer-agent`
Capability:
- `report.write`

Responsibility:
- accept an analysis artifact
- return a concise structured report artifact

## Registry model

Each agent record contains only the minimum needed for discovery:
- `name`
- `version`
- `description`
- `endpoint`
- `capabilities`
- `interaction_mode`

The registry record also carries minimal agent configuration:
- `system_prompt`
- `input_schema`
- `output_schema`
- `tool_refs`
- `model`
- `limits`

Registry metadata describes how the agent is found and invoked.
Agent configuration describes how the agent should behave at runtime.

Registration stores the agent base endpoint URL, not the `/invoke` path.
Capability search returns a list of matching agents.
For now, `interaction_mode` is descriptive metadata only: `callable`, `conversational`, or `both`.
The current runtime only invokes callable HTTP agents.

## Minimal artifact contract

Agent registration:

```json
{
  "name": "reader-agent",
  "version": "0.1.0",
  "description": "Reads inline CSV text and returns a normalized table artifact.",
  "endpoint": "http://reader-agent:8001",
  "capabilities": ["read.tabular"],
  "interaction_mode": "callable",
  "system_prompt": "Parse inline CSV into a structured table artifact.",
  "input_schema": {
    "type": "csv_text",
    "description": "Inline CSV text with a header row."
  },
  "output_schema": {
    "artifact_type": "table",
    "description": "Columns, rows, and row-count metadata."
  },
  "tool_refs": [],
  "model": "none",
  "limits": {
    "timeout": 10,
    "max_steps": 1
  }
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
    "row_count": 2,
    "column_count": 2,
    "source_format": "csv"
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
  ],
  "metadata": {
    "source_artifact_type": "table",
    "row_count": 2,
    "numeric_column_count": 1,
    "finding_count": 1
  }
}
```

Report writer output:

```json
{
  "artifact_type": "report",
  "summary": "Analyzed 2 rows across 1 numeric columns.",
  "sections": [
    {
      "title": "Key Findings",
      "content": "Column sales has average 90 across 2 numeric values."
    },
    {
      "title": "Column: sales",
      "content": "count=2, sum=180, average=90, min=80, max=100"
    }
  ],
  "metadata": {
    "source_artifact_type": "analysis",
    "row_count": 2,
    "numeric_column_count": 1,
    "section_count": 2
  }
}
```

Current artifact conventions:
- every artifact includes `artifact_type`
- every artifact includes `metadata`
- `table` carries `columns`, `rows`, and metadata about row count, column count, and source format
- `analysis` carries `metrics`, `findings`, and metadata about source type, numeric coverage, and finding count
- `report` carries `summary`, `sections`, and metadata about the source analysis and rendered section count

## Local run

Start the four long-running services:

```bash
docker compose up --build
```

In another terminal, run the registry-driven demo:

```bash
docker compose run --rm orchestrator
```

The orchestrator registers `reader-agent`, `math-agent`, and `report-writer-agent`, finds each one through registry capability lookup, sends inline CSV to the reader, passes the table artifact to the math agent, passes the analysis artifact to the report writer, and prints the final report artifact.

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
