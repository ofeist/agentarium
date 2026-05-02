# Owner Approval And Start: TASK-0007

- actor: `builder-organizer-a`
- date: `2026-05-02`
- status: `in_progress`

## Summary
`TASK-0007` is approved and implementation has started on `feature/task-0007-normalize-agent-metadata`.

## Locked Direction
- normalize only the existing three `registry/agents/*.yaml` files
- match the live `AgentRegistration` shape
- add focused validation coverage
- do not load metadata files at runtime
- do not add catalog, packaging, schema-framework, or marketplace behavior
