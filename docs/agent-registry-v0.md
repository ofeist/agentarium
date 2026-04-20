# Agent Registry v0

## Purpose

Agent registry stores shareable agents.

## Non-goals

Registry does not store:

- secrets
- runtime state
- traces
- memory

## Minimal agent entry

Each agent must define:

- `name`
- `version`
- `purpose`
- `inputs`
- `outputs`
- `runtime_type`

Optional for current MVP:

- `prompt_ref`
- `mcp_dependencies`
- `a2a`

## Field meanings

- `name`: unique agent name
- `version`: agent version
- `purpose`: one clear sentence what the agent does
- `inputs`: expected inputs
- `outputs`: returned outputs
- `runtime_type`: how the agent runs
- `prompt_ref`: path to prompt file, if applicable
- `mcp_dependencies`: MCP capabilities/services this agent needs, if any
- `a2a`: whether the agent is exposed to other agents and under which role, if applicable

## Runtime types

Initial values:

- `generic-llm-agent`
- `packaged-agent`

## Notes

- Agent is not the same thing as a Docker image
- Docker image is one possible runtime/deployment artifact
- MCP and A2A are external standards that Agentarium references, not redefines

