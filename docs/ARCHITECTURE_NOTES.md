# Architecture Notes

This note captures the current `agentarium` MVP architecture and immediate direction. It is not a full specification.

## Current MVP

The current MVP has these parts:

- `registry`: FastAPI service with in-memory agent registration, listing, capability search, and explicit agent configuration fields
- `reader-agent`: FastAPI service that accepts inline CSV and returns a normalized JSON table artifact
- `math-agent`: FastAPI service that accepts a table artifact and returns simple numeric metrics and findings
- `report-writer-agent`: FastAPI service that accepts an analysis artifact and returns a concise structured report artifact
- `orchestrator`: one-shot Python script that registers agents, resolves them by capability, invokes them over HTTP, and prints the final artifact
- `Docker Compose`: local runtime wrapper for starting services and running the orchestrator

The flow is intentionally small:

1. register agents in the registry
2. resolve them by capability
3. invoke them over HTTP
4. pass JSON artifacts from one agent to the next

## Current artifact conventions

The current MVP artifact contracts stay intentionally small, but they now follow a slightly clearer shared pattern:

- every artifact includes `artifact_type`
- every artifact includes `metadata`
- `table` includes `columns`, `rows`, and metadata with `row_count`, `column_count`, and `source_format`
- `analysis` includes `metrics`, `findings`, and metadata with `source_artifact_type`, `row_count`, `numeric_column_count`, and `finding_count`
- `report` includes `summary`, `sections`, and metadata with `source_artifact_type`, `row_count`, `numeric_column_count`, and `section_count`

This is still descriptive MVP structure, not a schema framework or standard.

## What the MVP has validated

So far, the MVP validates that:

- agents can be registered with explicit metadata/config
- agents can be discovered by capability
- a small registry-driven flow can chain three callable agents
- JSON artifact handoff works for the current structured-data slice
- Docker Compose is enough as an initial local multi-service runtime

It does **not** yet validate production deployment, persistence, auth, ranking, remote agents, or generalized interoperability.

## Minimal agent record

The current registry record includes:

- `name`
- `version`
- `description`
- `endpoint`
- `interaction_mode`
- `system_prompt`
- `capabilities`
- `input_schema`
- `output_schema`
- `tool_refs`
- `model`
- `limits`

Important clarification:

The prompt is part of agent configuration, but it is not the whole agent identity.

A useful agent record should describe:

- what the agent is
- what it does
- what it expects
- what it returns
- what tools/model it depends on
- what runtime limits apply

For this MVP slice, `input_schema` and `output_schema` are descriptive only, not full JSON Schema.

## Interaction modes

Current interaction modes are:

- `callable`
- `conversational`
- `both`

The MVP currently implements only callable HTTP agents.  
`interaction_mode` is descriptive metadata only for now.

## Runtime packaging vs agent identity

An agent is **not** the same thing as a Docker image.

A Docker image is one possible runtime/deployment artifact for an agent, but the registry entry should describe the **agent itself**, not force one packaging model too early.

Useful separation:

- **agent identity** = what the agent is, what it does, what it expects, what it returns
- **runtime model** = how the agent is executed
- **deployment artifact** = container image, local process, remote service, etc.

## Why Docker was the right MVP choice

Starting with Docker Compose was still the right choice because it immediately solved:

- network-level communication between agents/services
- reproducible local execution
- simple service addressing
- isolation between runtime components

Docker is a strong MVP runtime foundation.

But:

- Docker is a deployment/runtime choice
- Docker should not define the full ontology of an agent

## Likely runtime categories

Two runtime categories currently seem useful.

### Packaged agents

Agents with their own implementation/runtime artifact, for example:

- their own Docker image
- their own codebase
- their own service process

Examples:
- PR review agent
- statistics agent
- importer agent

### Generic runtime agents

Agents that run on a shared generic host/runtime and are mainly defined by configuration, for example:

- prompt
- MCP dependencies
- A2A exposure/role
- input/output contract
- model/runtime settings

Examples:
- reader agent
- report-writer agent
- summarizer agent

## Current direction

For now, the registry should continue to store **agents**.

But agent entries should eventually support different runtime styles, instead of assuming that every agent is packaged the same way.

A useful future direction is to make runtime type explicit, for example:

- `packaged-agent`
- `generic-llm-agent`

This should be treated as a runtime/deployment concern, not as the core definition of the agent itself.

## Open questions

Still open:

- how agent configuration is stored and versioned
- how runtime state evolves separately from registry metadata
- how to select among multiple agents with the same capability
- how to represent larger inputs, binary data, streaming, or external object references
- how far registry contracts should go in later iterations

## Non-goals for now

Agentarium is intentionally **not** standardizing these yet:

- MCP
- A2A
- policy/RBAC
- OCI-like packaging
- persistence
- ranking/selection among multiple agents
- filesystem/S3/HTTP unified input abstraction

More precisely: Agentarium should later integrate with MCP/A2A, not redefine them.

## Practical implication for next steps

Next formalization work should likely include:

- making runtime type explicit in the registry model
- keeping agent identity separate from deployment artifact
- supporting both packaged and generic agents in the longer-term design
- avoiding premature lock-in to `agent = container image`
