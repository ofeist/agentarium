# Review Request: TASK-0005

- actor: `builder-organizer-a`
- date: `2026-05-02`
- status: `review`

## Summary
`TASK-0005` is implemented on `feature/task-0005-clarify-orchestrator-flow` and ready for reviewer verification.

## What changed
- replaced repeated orchestrator lookup/invoke blocks with `resolve_required_agent()` and `invoke_agent()`
- fixed the pytest hang by removing FastAPI `TestClient` from service-level tests and calling local handlers/models directly
- kept the three composition steps explicit:
  - `read.tabular`
  - `analyze.basic-math`
  - `report.write`
- kept registration payloads in `orchestrator/run_demo.py`
- did not change README because commands, output intent, and behavior remain the same
- did not add unit tests because the helpers are thin HTTP wrappers and the Compose demo verifies the real flow

## Verification completed
- `pytest -q`
- `python3 -m py_compile orchestrator/run_demo.py`
- `docker compose config`
- `docker compose up --build -d`
- `docker compose run --rm orchestrator`
- `docker compose down`

## Review focus
- confirm the flow remains explicit and registry-driven
- confirm no workflow engine, DAG, pipeline config, retry framework, or broader orchestration system was introduced
- confirm no behavior change beyond readability cleanup
