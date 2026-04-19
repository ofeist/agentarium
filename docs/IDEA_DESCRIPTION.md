# Complete Idea Description

## Core idea

Build **agentarium**, an open agent registry that makes AI agents discoverable, describable, composable, and eventually deployable.

The long-term vision is similar to what package registries, Docker registries, and service catalogs did for software systems:
- package what exists
- describe what it does
- version it
- discover it
- connect it to other components
- build systems from reusable parts

## Main thesis

Today, many agents are still:
- ad-hoc scripts
- framework-specific objects
- tightly coupled to a single runtime
- hard to discover
- hard to compose
- hard to compare

An agent registry could become the missing discovery/composition layer.

## Working analogy to classic software infrastructure

### Traditional software stack
- Docker image = packaged service artifact
- Docker Hub / OCI registry = artifact distribution and discovery
- Docker Compose / Kubernetes = composition and orchestration
- service networking = service-to-service communication
- IAM/RBAC = permission model

### Agent stack analogy
- agent manifest = packaged agent description
- agent registry = discovery, capability lookup, compatibility metadata
- agent orchestrator = multi-agent workflow composition
- A2A = agent-to-agent communication
- MCP = agent-to-tool communication
- policy layer = trust, approvals, permissions, governance

## Registry purpose

A mature agent registry could support:
- capability-based discovery
- versioning and compatibility
- trust/provenance metadata
- internal/public agent catalogs
- composition into agent stacks
- deployment handoff metadata
- marketplace-like ecosystems later

## Why capability-first discovery matters

Unlike plain service discovery, agent systems benefit from semantic lookup.

Instead of asking:
- where is service X?

You ask:
- which agent can `read.tabular`?
- which agent can `analyze.math`?
- which agent can `report.write`?

That is the key conceptual shift.

## Long-term feature set

### Registry core
- agent identity
- versioning
- capability catalog
- endpoint/runtime reference
- publisher metadata
- compatibility metadata

### Extended metadata
- input/output schemas
- required tools
- optional tools
- stateful/stateless hints
- cost/latency hints
- trust/policy profile
- deployment/runtime hints

### Composition features
- find matching agents for a workflow step
- rank alternatives
- validate compatibility between agent outputs and inputs
- describe agent stacks declaratively

### Governance features
- verified publishers
- signing/provenance
- approval classes
- internal-only visibility
- production approval status

## Minimal path to long-term vision

The MVP deliberately starts much smaller:
- 2 agents
- 1 registry
- 1 orchestrator
- 1 shared artifact contract

If that works, the project can grow toward:
1. richer registry metadata
2. agent manifests
3. agent stack definitions
4. interoperability with A2A and MCP
5. optional deployment/runtime integration

## Why open source

Open source makes sense here because:
- interoperability and standardization benefit from public discussion
- schemas and APIs need scrutiny
- the project gains credibility if the core model is public
- others may contribute manifests, examples, and integrations

## Practical positioning

Short positioning line:

> agentarium is an open agent registry and capability catalog for discovering, composing, and routing AI agents.
