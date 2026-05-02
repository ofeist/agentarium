# Owner Approval And Start: TASK-0006

- actor: `builder-organizer-a`
- date: `2026-05-02`
- status: `in_progress`

## Summary
`TASK-0006` is approved and implementation has started on `feature/task-0006-runtime-type`.

## Locked Direction
- make `runtime_type` required in the live registry registration model
- allow only `packaged-agent` and `generic-llm-agent`
- use `packaged-agent` for the three current FastAPI services
- align only `runtime_type` in placeholder YAML files
- keep the field descriptive only and do not branch runtime behavior on it
