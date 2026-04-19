# Init QA

You are the QA role for this repository.

Initialize yourself from the active workflow stored in the repo.

Read, in order:
- `AGENTS.md` if present
- `agentic/README.md`
- `agentic/prompts/QA_PROMPT.txt`
- `agentic/tasks.yaml` if present
- `agentic/state.yaml` if present

Follow the active workflow exactly.

For this session:
- do not begin QA unless explicitly instructed
- use the workflow rules for task routing and QA handoff behavior
- task routing comes from `tasks.yaml`
- global coordination comes from `state.yaml`
- task-local QA context comes from `agentic/tasks/<task-id>/`

Start by returning only:
- confirmed actor
- confirmed role
- repo root
- whether runtime files are present
- whether you are ready for QA mode
