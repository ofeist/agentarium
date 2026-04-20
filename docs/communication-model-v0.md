# Communication Model v0

## Purpose

This note defines the current minimal communication model for Agentarium.

It is intentionally small and based on the current MVP.

## Communication types

### 1. Orchestrator -> agent

This is the current MVP control flow.

The orchestrator:

- selects the next agent
- sends input to that agent
- receives the output
- passes the output to the next step

This is currently the main execution model.

### 2. Agent -> agent

This is future-facing A2A-style communication.

For now, agents do not freely talk to each other.

If agent-to-agent communication is introduced later, it should be explicit and structured.

### 3. Agent -> tool/service

This is how an agent uses external capabilities.

Examples:

- MCP service
- HTTP API
- database-backed service

In the current MVP this may still be plain HTTP, even if later it maps more cleanly to MCP-style tool access.

## Current MVP rule

For now:

- agents do not self-route
- agents do not freely call each other
- the orchestrator drives the chain

This keeps execution simple and inspectable.

## Minimal handoff shape

When one step passes work to the next, the payload should be thought of as containing:

- `task`
- `summary`
- `artifact_ref` or structured result
- `status`

This does not need to be heavily formalized yet, but it should stay small and predictable.

## Non-goals for now

This model does not yet define:

- memory
- long-running conversations
- autonomous agent negotiation
- judge/reviewer loops
- dynamic multi-agent routing
- full A2A protocol support
- full MCP protocol support

## Notes

- A2A remains the future direction for explicit agent-to-agent communication
- MCP remains the future direction for tool/service access
- Agentarium does not redefine either of them
- the current MVP uses a small orchestrator-led flow because it is easier to reason about

