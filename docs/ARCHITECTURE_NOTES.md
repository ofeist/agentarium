# Architecture Notes

This note captures the current `agentarium` MVP architecture and the immediate direction. It is not a full specification.

## Current MVP Architecture

The current MVP has five moving parts:

- registry: FastAPI service with in-memory agent registration, listing, capability search, and explicit agent configuration fields.
- reader-agent: FastAPI service that accepts inline CSV and returns a normalized JSON table artifact.
- math-agent: FastAPI service that accepts a table artifact and returns simple numeric metrics and findings.
- report-writer-agent: FastAPI service that accepts an analysis artifact and returns a concise structured report artifact.
- orchestrator: one-shot Python script that registers agents, resolves them by capability, invokes them over HTTP, and prints the final artifact.
- Docker Compose: local runtime wrapper for starting the services and running the orchestrator.

The flow is intentionally small:

1. orchestrator registers agent base endpoint URLs, capabilities, descriptive interaction mode, and minimal config in the registry
2. orchestrator searches the registry by capability
3. orchestrator invokes the returned agent endpoint over HTTP
4. reader-agent returns a JSON table artifact
5. orchestrator passes that artifact to math-agent
6. math-agent returns a JSON analysis artifact
7. orchestrator searches the registry for `report.write`
8. orchestrator passes the analysis artifact to report-writer-agent
9. report-writer-agent returns a JSON report artifact

## What The MVP Has Validated

- agents can be registered with minimal metadata
- agents can be discovered by capability
- a small registry-driven flow can chain three callable agents
- JSON artifact handoff works well for the current structured-data slice
- Docker Compose is enough as the first local multi-service runtime wrapper

This does not validate production deployment, multi-tenant registries, remote agents, auth, ranking, persistence, or generalized interoperability.

## Minimal Agent Configuration

Agent identity and configuration are now represented directly in the registry record. The current minimal fields are:

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
- `limits`, for example `timeout` and `max_steps`

The prompt is part of agent configuration, but it should not be the whole agent identity. A useful agent record needs to describe what the agent is, what it can do, what it expects, what it returns, what tools or model it depends on, and what runtime limits apply.

Registry metadata fields are `name`, `version`, `description`, `capabilities`, `interaction_mode`, and `endpoint`.
Agent config fields are `system_prompt`, `input_schema`, `output_schema`, `tool_refs`, `model`, and `limits`.

For this slice, `input_schema` and `output_schema` are simple descriptive objects, not full JSON Schema. `model` is a simple string.

## Interaction Modes

Not all agents should expose the same interaction shape. A simple initial model is:

- `callable`: invoked with a structured input and returns a structured output.
- `conversational`: maintains a user-facing conversation interface.
- `both`: can be called as a worker and can also participate conversationally.

Worker agents are usually `callable`. Some specialist agents may be `conversational` when iterative clarification is central to their role. A front or manager agent may expose conversation to a user while delegating internally to callable worker agents.

The current MVP implements only callable HTTP agents. `interaction_mode` is descriptive metadata only; it does not introduce conversational runtime behavior.

## Architecture Skeleton / Direction

Already implemented:

- agent registry with in-memory storage
- HTTP agent runtime for the MVP services
- explicit agent registration/configuration contract
- JSON contracts/artifacts for table and analysis payloads
- JSON report artifact for the final presentation/output layer
- orchestrator-driven stack composition
- Docker Compose as the local runtime wrapper

Intended next:

- more precise artifact contracts as use cases require them
- clearer use of the config fields by actual agent runtimes

Still open / not yet decided:

- how agent configuration is stored and versioned
- how runtime state should evolve separately from registry metadata
- how to select among multiple agents with the same capability
- how to represent larger inputs, binary data, streaming, or external object references
- whether a future input abstraction should cover filesystem, S3, HTTP, or other sources

Future input abstraction may matter later, but it is not part of the current MVP core.

## Non-Goals For Now

The project is intentionally not standardizing these yet:

- A2A
- MCP
- policy/RBAC
- OCI-like packaging
- persistence
- ranking or selection among multiple agents
- filesystem/S3/HTTP unified input abstraction

## Runtime packaging vs agent identity

One important clarification from the current MVP work:

An agent is **not the same thing** as a Docker image.

A Docker image is one possible **runtime/deployment artifact** for an agent, but the registry entry should describe the **agent itself**, not force one packaging model too early.

This distinction matters because the same logical agent may later be run in different ways:

- as a Docker container
- as a local Python process
- as a remote service
- as a generic LLM runtime with prompt/config injection
- as some future serverless or hosted execution model

So for Agentarium we should keep these layers separate:

- **agent identity** = what the agent is, what it does, what it expects, what it returns
- **runtime model** = how the agent is executed
- **deployment artifact** = container image, local process, remote service, etc.

## Why Docker was still the right MVP choice

Starting with Docker Compose was still a good decision.

It solved real early problems immediately:

- network-level communication between agents/services
- reproducible local execution
- simple service addressing
- isolation between runtime components
- a practical way to stand up a small multi-agent stack

So Docker remains a strong MVP foundation.

But the current view is:

- Docker is a **great runtime/deployment starting point**
- Docker should **not define the full ontology of what an agent is**

## Likely runtime categories

At the moment, two runtime categories seem useful.

### 1. Packaged agents

These are agents with their own implementation/runtime artifact, for example:

- their own Docker image
- their own codebase
- their own service process
- stronger specialization and more stable behavior

Examples might later include things like:

- PR review agent
- statistics agent
- importer agent

### 2. Generic runtime agents

These are agents that run on a shared generic host/runtime and are mainly defined by configuration, for example:

- prompt
- MCP dependencies
- A2A exposure/role
- input/output contract
- model/runtime settings

This makes lightweight agents easier to create, modify, and share without building a dedicated image each time.

Examples might later include things like:

- reader agent
- report-writer agent
- summarizer agent

## Current architectural direction

For now, the registry should continue to store **agents**.

But agent entries should eventually allow different runtime styles, instead of assuming that every agent is packaged the same way.

A useful future direction is to make runtime type explicit, for example with concepts such as:

- `packaged-agent`
- `generic-llm-agent`
- possibly later other runtime types

This should be treated as a runtime/deployment concern, not as the core definition of the agent itself.

## Practical implication for next steps

This means the next formalization work should likely include:

- making runtime type explicit in the registry model
- keeping agent identity separate from deployment artifact
- supporting both packaged and generic agents in the longer-term design
- avoiding premature lock-in to "agent = container image"
