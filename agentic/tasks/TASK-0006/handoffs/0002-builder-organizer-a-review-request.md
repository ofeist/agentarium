# Review Request: TASK-0006

- actor: `builder-organizer-a`
- date: `2026-05-02`
- status: `review`

## Summary
`TASK-0006` is implemented on `feature/task-0006-runtime-type` and ready for reviewer verification.

## What changed
- added required `runtime_type` live registry metadata to `AgentRegistration`
- allowed `runtime_type` values are `packaged-agent` and `generic-llm-agent`
- updated current orchestrator registrations to use `packaged-agent`
- added registry tests for storing `runtime_type`, missing `runtime_type`, and invalid `runtime_type`
- aligned only the `runtime_type` values in `registry/agents/*.yaml` to `packaged-agent`
- updated concise README and architecture notes

## Verification completed
- `pytest -q`
- `python3 -m py_compile registry/app.py orchestrator/run_demo.py`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`

## Review focus
- confirm `runtime_type` is required, validated, and returned by the registry
- confirm current live registrations use `packaged-agent`
- confirm `runtime_type` is descriptive only and no runtime behavior branches on it
- confirm placeholder YAML cleanup is limited to `runtime_type`
- confirm no packaging, deployment, generic runtime, A2A, MCP, persistence, UI, or marketplace scope was added
