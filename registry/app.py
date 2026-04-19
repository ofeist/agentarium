from typing import Annotated
from urllib.parse import urlparse

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="agentarium-registry")


class AgentRegistration(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    endpoint: str = Field(min_length=1)
    capabilities: list[str] = Field(min_length=1)

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("endpoint must be an absolute http(s) base URL")
        if parsed.path not in {"", "/"}:
            raise ValueError("endpoint must be the agent base URL, not an invoke path")
        return value.rstrip("/")

    @field_validator("capabilities")
    @classmethod
    def validate_capabilities(cls, value: list[str]) -> list[str]:
        cleaned = [capability.strip() for capability in value if capability.strip()]
        if not cleaned:
            raise ValueError("at least one capability is required")
        return cleaned


AgentRecord = AgentRegistration

AGENTS: list[AgentRecord] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/agents", response_model=AgentRecord)
def register_agent(agent: AgentRegistration) -> AgentRecord:
    for index, existing in enumerate(AGENTS):
        if existing.name == agent.name and existing.version == agent.version:
            AGENTS[index] = agent
            return agent

    AGENTS.append(agent)
    return agent


@app.get("/agents", response_model=list[AgentRecord])
def list_agents() -> list[AgentRecord]:
    return AGENTS


@app.get("/search", response_model=list[AgentRecord])
def search_agents(
    capability: Annotated[str, Query(min_length=1)],
) -> list[AgentRecord]:
    return [agent for agent in AGENTS if capability in agent.capabilities]
