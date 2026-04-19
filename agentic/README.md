# Agentic Workflow

This is the active workflow scaffold for this repository.

The workflow is task-centric, worktree-aware, and multi-agent aware from the start, even when used by one person or one agent.

## Active Structure

```text
agentic/
  README.md
  PORTING.md
  bootstrap-runtime.sh
  state.example.yaml
  tasks.example.yaml
  agent-config.example.yaml
  prompts/
    BUILDER_ORGANIZER_PROMPT.txt
    REVIEWER_PROMPT.txt
    QA_PROMPT.txt
    init-builder-organizer.md
    init-reviewer.md
    init-qa.md
  workflows/
    WORKTREE_POLICY.md
    PORTING.md
  tasks/
    _template/
      TASK.md
      handoffs/
        0001-builder-organizer-a-start.md
```

Runtime files for a live repo may later look like:

```text
agentic/
  state.yaml
  tasks.yaml
  agent-config.yaml
  tasks/
    TASK-0001/
      TASK.md
      handoffs/
        0001-builder-organizer-a-start.md
```

Initialize the live runtime files with:

```bash
bash agentic/bootstrap-runtime.sh
```

## Runtime File Lifecycle

### `*.example.yaml` Files

- `agentic/state.example.yaml`, `agentic/tasks.example.yaml`, and `agentic/agent-config.example.yaml` are committed scaffold files
- they define the baseline shape for fresh runtime initialization
- they are portable and should be copied when this workflow is ported to another repo
- they are not the active coordination state for a running repo

### Live Runtime Files

- `agentic/state.yaml`, `agentic/tasks.yaml`, and `agentic/agent-config.yaml` are live runtime files for the current repo
- in the active workflow, these live runtime files are committed repo state because they are the shared source of truth used by agents and humans coordinating work
- live runtime files are repo-specific and should not be copied into a different repo as part of workflow porting
- task instances under `agentic/tasks/<task-id>/` and their handoff history are also live repo-specific runtime history

### Commit Policy

- commit the workflow scaffold:
  - `agentic/README.md`
  - `agentic/*.example.yaml`
  - prompts, workflow docs, and templates
- commit the live runtime files for the active repo:
  - `agentic/state.yaml`
  - `agentic/tasks.yaml`
  - `agentic/agent-config.yaml`
  - active task folders and task-local handoffs
- do not treat one repo's live runtime files or task history as portable defaults for another repo

### Initialization Policy

- in a new repo that has the workflow scaffold but no live runtime files yet, initialize the live runtime files by running `bash agentic/bootstrap-runtime.sh`
- the bootstrap script copies each `*.example.yaml` file to its live runtime counterpart once and refuses to overwrite an existing live runtime file
- on a new machine for an already initialized repo, use the live runtime files that come from the repo checkout or a fresh pull
- do not rerun the bootstrap script on an already initialized repo unless the live runtime files are intentionally absent
- if a repo is being ported or created fresh, start from the committed example files and initialize fresh live runtime state for that repo

## Core Model

- `state.yaml` is the global coordination snapshot.
- `tasks.yaml` is the registry of active tasks.
- `agent-config.yaml` enables roles and documents startup conventions for those roles.
- `tasks/<task-id>/TASK.md` holds task scope and acceptance criteria.
- `tasks/<task-id>/handoffs/` holds task-local coordination history.
- one handoff event = one file
- one active branch has one writer at a time
- parallel work is allowed only when write scopes do not overlap

## Rules

- all new tasks must use `agentic/tasks/<task-id>/`
- legacy top-level handoffs are reference-only
- `agent-config.yaml` does not assign work
- `tasks.yaml` is the authoritative source for task assignment and positioning

## Metadata Precedence

- `state.next_actor` is the global next actor
- `tasks[].next_actor` is the next actor for that specific task
- when a task reaches `done`, set `tasks[].next_actor` to `null`
- task routing comes primarily from `tasks.yaml`
- `agent-config.yaml` defines enabled role configuration and optional prompt metadata

## Naming Conventions

- linked worktrees live under the repo-local `worktrees/` directory
- worktrees use `worktrees/<repo>-<task-id>-<actor-id>`
- branches use `<type>/<task-id>-<slug>`
- task handoff files use `NNNN-<actor-id>-<event>.md`

## Task ID Rule

- task ids use `TASK-####`
- determine the next id from the set of existing identifiers under `agentic/tasks/` whose basename matches `TASK-####` or starts with `TASK-####-`
- ignore `_template`, `TASK_TEMPLATE.md`, and any path outside that `TASK-####` namespace
- the next task id is the next zero-padded number in that sequence

## Branch Naming Rule

- allowed task types are `feature`, `fix`, `chore`, and `docs`
- branches use `<type>/<task-id>-<slug>`
- examples:
  - `feature/task-0001-bootstrap-runtime-files`
  - `fix/task-0002-correct-task-routing`
  - `chore/task-0003-align-worktree-policy`
  - `docs/task-0004-clarify-builder-prompt`

## Agent Config Note

- `agentic/agent-config.example.yaml` is the committed scaffold source for initialization
- `agentic/agent-config.yaml` is the live runtime file used by the active repo after initialization
- under the current workflow, `agent-config.yaml` follows the same live-runtime lifecycle as `state.yaml` and `tasks.yaml`

## Initial Role

The initial active role is `Builder-Organizer`.

That role:
- implements the slice
- keeps task coordination current
- writes explicit handoff files for checkpoints, blockers, review requests, and completion
- commits and pushes coherent slice boundaries and meaningful workflow-state transitions, including approved `draft` -> `ready` transitions
- follows the worktree policy

## Reviewer

Reviewer initialization comes from `agentic/prompts/init-reviewer.md`.

Reviewer reads, in order:
- `AGENTS.md` if present
- `agentic/README.md`
- `agentic/prompts/REVIEWER_PROMPT.txt`
- `agentic/tasks.yaml`
- `agentic/state.yaml`
- the assigned task folder under `agentic/tasks/<task-id>/`

Reviewer is used after Builder execution for a reviewable slice.

Reviewer:
- reviews only
- does not implement
- does not change task scope
- writes findings and review outcomes in task-local handoff files
- commits and pushes completed review handoff artifacts so the review is visible to other agents
- stops and reports instead of committing if unrelated working-tree changes make a review-only commit unsafe

Minimal reviewability rule:
- a task is reviewable when it has entered execution and the Builder has finished the current reviewable slice
- `approve` means no material issues were found for the approved slice
- `changes_requested` means the slice must go back to Builder for fixes before approval
- `blocked` means review cannot proceed because required review context, routing, or reviewable task state is missing or inconsistent

## QA

QA initialization comes from `agentic/prompts/init-qa.md`.

QA reads, in order:
- `AGENTS.md` if present
- `agentic/README.md`
- `agentic/prompts/QA_PROMPT.txt`
- `agentic/tasks.yaml`
- `agentic/state.yaml`
- the assigned task folder under `agentic/tasks/<task-id>/`

QA is distinct from Reviewer:
- Reviewer checks the slice against the approved task contract and scope
- QA checks verification quality, operational readiness, and unverified risk or gaps
- QA should not simply repeat Reviewer findings unless they directly affect verification or readiness

QA:
- is read-only by default
- does not implement
- does not change task scope
- writes only task-local QA handoff files
- may commit and push only those QA handoff artifacts

Minimal QA outcome rule:
- `pass` means verification is sufficient for the slice and no material readiness gaps were found
- `issues_found` means verification or readiness gaps should be addressed before relying on the slice
- `blocked` means QA cannot proceed because required context, environment, or task state is missing or inconsistent

## Minimal Flow

1. Copy `agentic/state.example.yaml` to `agentic/state.yaml` if runtime state has not been initialized yet.
2. Copy `agentic/tasks.example.yaml` to `agentic/tasks.yaml` if the task registry has not been initialized yet.
3. Copy `agentic/agent-config.example.yaml` to `agentic/agent-config.yaml` if role activation config has not been initialized yet.
4. Copy `agentic/tasks/_template/` to `agentic/tasks/<next-task-id>/`.
5. Fill in `TASK.md` and open the task in `draft`.
6. Create or update `tasks.yaml` with the new task in `draft` and `next_actor: null`.
7. Move the task to `ready` only after explicit approval to start implementation.
8. Begin execution only when the task is `ready`; at that point Builder-Organizer moves it to `in_progress`.
9. Write the first execution-start handoff only when the task moves from `ready` to `in_progress`.
10. Hand off or close the task explicitly.

The bootstrap script initializes missing live runtime files from the committed example files and refuses to overwrite existing runtime files.

## Startup Model

An agent should initialize in this order:

1. Read `agent-config.yaml` to see which roles are enabled and any optional prompt metadata for those roles.
2. Read `tasks.yaml` to determine task ownership, branch, worktree, and task-level next actor.
3. Read `state.yaml` to understand the global objective, blockers, and global next actor.
4. Read the selected task folder to execute the task and record task-local handoffs.

Use `done` only when the task is actually complete and the completion handoff has been written.

## Task Opening Workflow

- opening a task is administrative, not execution
- a newly opened task starts as `draft`
- the minimum task-opening artifacts are:
  - `agentic/tasks/<task-id>/TASK.md`
  - a task entry in `tasks.yaml`
- the canonical task template also supports optional shaping and approval fields such as roadmap reference, rollout class, slice readiness check, open questions, and rollout notes
- a task in `draft` must not be implemented yet
- a task may be executed only after it has been explicitly moved to `ready`
- when Builder-Organizer actually begins work, it moves the task from `ready` to `in_progress`
- the first execution-start handoff is written only when the task moves from `ready` to `in_progress`

## Thin Slice Rule

A task should be small enough that:
- its goal is clear
- its scope is narrow
- its blast radius is low
- it can be reviewed and reasoned about easily
- it fits one clear branch/worktree execution stream

## Reopen vs New Task

- reopen the same task if the goal and scope are still the same and the task needs correction, finishing, or completion within that same intended slice
- create a new task id if the follow-up is a new slice, the goal changes, the scope expands materially, or the new work should be tracked independently

## Builder-Organizer Return Format

Startup:
- Actor: `<actor-id>`
- Role: `Builder-Organizer`
- Task: `<task-id>`
- Branch: `<branch>`
- Worktree: `<worktree>`
- Task Folder: `<task-folder>`
- Owner: `yes|no`
- Task Next Actor: `<actor-id>`
- Action: `<next planned action>`

Completion:
- Task: `<task-id>`
- Branch: `<branch>`
- Worktree: `<worktree>`
- Handoff: `<handoff-file-path>`
- Tasks Updated: `yes|no`
- State Updated: `yes|no`
- Verification: `<short result>`
- Next Actor: `<actor-id>`
- Outcome: `<ready_for_review|blocked|done|in_progress>`

## Legacy Material

The following remain in the repo as reference material during migration:
- legacy v1 task files and handoff examples
- legacy top-level handoff docs and templates under `agentic/handoffs/`
- legacy v1 prompt files such as `BUILDER_PROMPT.txt` and `PLANNER_PROMPT.txt`
- `agentic/experiments/workflow-v2/`

New workflow changes should use the structure described in this file.
