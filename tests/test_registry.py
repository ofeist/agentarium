import pytest
from pydantic import ValidationError

from conftest import load_app_module


def agent_payload(**overrides):
    payload = {
        "name": "reader-agent",
        "version": "0.1.0",
        "description": "Reads inline CSV text.",
        "endpoint": "http://reader-agent:8001",
        "capabilities": ["read.tabular"],
        "interaction_mode": "callable",
        "system_prompt": "Parse inline CSV into a table artifact.",
        "input_schema": {
            "type": "csv_text",
            "description": "Inline CSV text with a header row.",
        },
        "output_schema": {
            "artifact_type": "table",
            "description": "Structured table artifact.",
        },
        "tool_refs": [],
        "model": "none",
        "limits": {"timeout": 10, "max_steps": 1},
    }
    payload.update(overrides)
    return payload


def test_registry_search_returns_matching_agents_by_capability():
    registry = load_app_module("registry_app", "registry/app.py")
    registry.AGENTS.clear()

    registry.register_agent(registry.AgentRegistration(**agent_payload()))
    registry.register_agent(
        registry.AgentRegistration(
            **agent_payload(
                name="math-agent",
                description="Computes basic numeric metrics.",
                endpoint="http://math-agent:8002",
                capabilities=["analyze.basic-math"],
                system_prompt="Analyze table artifacts.",
                input_schema={"artifact_type": "table"},
                output_schema={"artifact_type": "analysis"},
            )
        )
    )

    matches = registry.search_agents(capability="read.tabular")

    assert [agent.model_dump(mode="json") for agent in matches] == [agent_payload()]


def test_registry_registration_stores_metadata_and_config_fields():
    registry = load_app_module("registry_app_config", "registry/app.py")
    registry.AGENTS.clear()

    response = registry.register_agent(
        registry.AgentRegistration(
            **agent_payload(
                interaction_mode="both",
                tool_refs=["calculator"],
                model="gpt-example",
                limits={"timeout": 20, "max_steps": 3},
            )
        )
    )

    body = response.model_dump(mode="json")
    assert body["name"] == "reader-agent"
    assert body["description"] == "Reads inline CSV text."
    assert body["capabilities"] == ["read.tabular"]
    assert body["interaction_mode"] == "both"
    assert body["endpoint"] == "http://reader-agent:8001"
    assert body["system_prompt"] == "Parse inline CSV into a table artifact."
    assert body["input_schema"]["type"] == "csv_text"
    assert body["output_schema"]["artifact_type"] == "table"
    assert body["tool_refs"] == ["calculator"]
    assert body["model"] == "gpt-example"
    assert body["limits"] == {"timeout": 20, "max_steps": 3}


def test_registry_rejects_unknown_interaction_mode():
    registry = load_app_module("registry_app_interaction_mode", "registry/app.py")
    registry.AGENTS.clear()

    with pytest.raises(ValidationError):
        registry.AgentRegistration(
            **agent_payload(interaction_mode="background-daemon")
        )
