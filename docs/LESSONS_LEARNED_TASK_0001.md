# Lessons Learned From TASK-0001

TASK-0001 built the first runnable `agentarium` MVP: an in-memory registry, a reader-agent, a math-agent, and an orchestrator that uses registry capability lookup before invoking agents.

This note records what the MVP actually validated and what remains only a hypothesis.

## 1. Capability Lookup Worked For Simple Composition

What we observed:
The orchestrator registered both agents, searched the registry by `read.tabular` and `analyze.basic-math`, and used the returned endpoint URLs to invoke each agent.

Why it matters:
This was enough to remove hardcoded agent routing from the demo flow. Even with only two agents, capability lookup gave the orchestrator a clear discovery step instead of binding directly to a named service.

What it suggests next:
Keep capability lookup as the central composition mechanism for the next slice, but do not assume it is sufficient for selection when multiple agents provide the same capability. Ranking, compatibility checks, and richer metadata remain unvalidated.

## 2. JSON Artifact Handoff Was Cleaner Than File Paths

What we observed:
The reader-agent returned a structured table artifact as JSON, and the math-agent consumed that artifact directly over HTTP. No shared filesystem, mounted file path, or path translation was needed between containers.

Why it matters:
For this MVP, JSON artifacts kept the agent boundary explicit and made the handoff easy to test at the service level. The contract was visible in request and response payloads instead of being hidden behind local file assumptions.

What it suggests next:
Keep JSON artifacts for small structured handoffs. Larger files, binary payloads, streaming data, or external object storage remain untested and should not be designed prematurely from this MVP alone.

## 3. Docker Compose Was Enough For The First Local Stack

What we observed:
`docker compose up --build` started the three long-running services, and `docker compose run --rm orchestrator` completed the demo through Compose service names.

Why it matters:
Compose provided enough isolation and networking to validate the local multi-service shape without introducing deployment infrastructure or orchestration complexity.

What it suggests next:
Continue using Compose as the local development wrapper while the system remains small. This does not validate production deployment, scaling, health orchestration, service restarts, or remote agent execution.

## 4. The Contracts Were Helpful But Still Thin

What we observed:
Minimal Pydantic models caught basic shape errors and documented the three main payloads: agent registration, table artifact, and analysis artifact. The contracts were enough for the demo and tests.

Why it matters:
Explicit payload shapes made the services easier to reason about without adding a shared schema package or framework. The implementation stayed small, and tests could assert behavior directly.

What it suggests next:
Add contract detail only when a new slice needs it. The current contracts do not yet cover schema versions, column types, error semantics, compatibility negotiation, or multiple artifact types.

## 5. Test Scope Needs To Match The Repo Layout

What we observed:
The service-level tests validated core behavior quickly, but plain `pytest` needed root configuration so it would not recurse into repo-local `worktrees/` and collect duplicate tests.

Why it matters:
The workflow layout affects developer commands. A passing test suite is not just about test content; collection boundaries must also match the repository structure.

What it suggests next:
Keep the current service-level tests as the fast baseline. Add integration automation only when it catches a real risk beyond what the Compose demo already exercises.

## Still Unproven

- whether capability lookup remains useful when multiple agents match the same capability
- how artifact contracts should evolve across versions
- how to handle large files, binary data, or streaming inputs
- whether this registry model is enough for remote or production agents
- auth, policy, persistence, A2A, MCP, ranking, and UI behavior
