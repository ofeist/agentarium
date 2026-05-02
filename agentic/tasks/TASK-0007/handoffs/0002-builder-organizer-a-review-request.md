# Review Request: TASK-0007

- actor: `builder-organizer-a`
- date: `2026-05-02`
- status: `review`

## Summary
`TASK-0007` is implemented on `feature/task-0007-normalize-agent-metadata` and ready for reviewer verification.

## What changed
- normalized the three existing `registry/agents/*.yaml` files to match the live `AgentRegistration` record shape
- removed obsolete placeholder fields such as `apiVersion`, `kind`, `metadata`, `spec`, `purpose`, `inputs`, `outputs`, `prompt_ref`, `mcp_dependencies`, and `a2a`
- kept all three agents as `runtime_type: packaged-agent`
- added a focused test that parses the YAML files and validates each one against `AgentRegistration`

## Verification completed
- `pytest -q`
- parsed all `registry/agents/*.yaml` files with PyYAML
- `git diff --check`

Docker Compose was not run because this task changes metadata files and tests only, with no runtime behavior changes.

## Review focus
- confirm the YAML files match the live registry record shape
- confirm obsolete placeholder fields are removed
- confirm the validation test is focused and does not imply runtime loading
- confirm no orchestrator behavior, registry endpoint, catalog, package, marketplace, A2A, MCP, or runtime behavior was added
