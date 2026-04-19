# MVP Description

## One-sentence MVP

agentarium is a tiny local agent stack that proves capability-based agent discovery and chaining through a registry.

## Minimal success criteria

The MVP is successful if the following works locally:

1. The registry starts.
2. Two agents start.
3. The orchestrator registers both agents.
4. The orchestrator searches the registry for `read.tabular`.
5. The orchestrator invokes the returned `reader-agent`.
6. The orchestrator searches the registry for `analyze.basic-math`.
7. The orchestrator invokes the returned `math-agent`.
8. The final analysis result is printed.

## What this MVP proves

- a registry can be used for **agent discovery**, not just listing
- **capability-based routing** is practical
- agents can communicate through a minimal shared artifact contract
- a multi-agent stack can be composed from small specialized services

## What this MVP intentionally does not prove

- universal agent interoperability
- a production-ready registry standard
- a business model
- large-scale orchestration
- security/governance
- dynamic skill negotiation

## Minimum implementation choices

- HTTP only
- FastAPI services
- in-memory or SQLite registry
- JSON payloads
- synchronous orchestration script
- Docker Compose for local startup

## Minimal components

### 1. Registry
Responsibilities:
- store agent metadata
- list agents
- search agents by capability

Minimum API:
- `POST /agents`
- `GET /agents`
- `GET /search?capability=...`
- `GET /health`

### 2. Reader agent
Responsibilities:
- parse CSV
- normalize rows
- output a `table` artifact

Minimum API:
- `POST /invoke`
- `GET /health`

### 3. Math agent
Responsibilities:
- consume `table` artifact
- compute basic numeric summary
- output an `analysis` artifact

Minimum API:
- `POST /invoke`
- `GET /health`

### 4. Orchestrator
Responsibilities:
- register agents
- resolve agents by capability
- call agents in sequence
- print final output

## Demo task

Example task:

> Read a CSV of regional sales and compute a basic sales summary.

## Time expectation

- ultra-thin version: 3-5 focused days
- cleaner version: 1-2 weeks
