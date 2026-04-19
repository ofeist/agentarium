# Architecture Notes

This note captures the current `agentarium` MVP architecture and the immediate direction. It is not a full specification.

## Current MVP Architecture

The current MVP has five moving parts:

- registry: FastAPI service with in-memory agent registration, listing, capability search, and explicit agent configuration fields.
- reader-agent: FastAPI service that accepts inline CSV and returns a normalized JSON table artifact.
- math-agent: FastAPI service that accepts a table artifact and returns simple numeric metrics and findings.
- orchestrator: one-shot Python script that registers agents, resolves them by capability, invokes them over HTTP, and prints the final artifact.
- Docker Compose: local runtime wrapper for starting the services and running the orchestrator.

The flow is intentionally small:

1. orchestrator registers agent base endpoint URLs, capabilities, descriptive interaction mode, and minimal config in the registry
2. orchestrator searches the registry by capability
3. orchestrator invokes the returned agent endpoint over HTTP
4. reader-agent returns a JSON table artifact
5. orchestrator passes that artifact to math-agent
6. math-agent returns a JSON analysis artifact

## What The MVP Has Validated

- agents can be registered with minimal metadata
- agents can be discovered by capability
- a small registry-driven flow can chain multiple agents
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
- HTTP agent runtime for the two MVP services
- explicit agent registration/configuration contract
- JSON contracts/artifacts for table and analysis payloads
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
