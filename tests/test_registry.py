from fastapi.testclient import TestClient

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
    client = TestClient(registry.app)

    client.post("/agents", json=agent_payload()).raise_for_status()
    client.post(
        "/agents",
        json=agent_payload(
            name="math-agent",
            description="Computes basic numeric metrics.",
            endpoint="http://math-agent:8002",
            capabilities=["analyze.basic-math"],
            system_prompt="Analyze table artifacts.",
            input_schema={"artifact_type": "table"},
            output_schema={"artifact_type": "analysis"},
        ),
    ).raise_for_status()

    response = client.get("/search", params={"capability": "read.tabular"})

    assert response.status_code == 200
    assert response.json() == [agent_payload()]


def test_registry_registration_stores_metadata_and_config_fields():
    registry = load_app_module("registry_app_config", "registry/app.py")
    registry.AGENTS.clear()
    client = TestClient(registry.app)

    response = client.post(
        "/agents",
        json=agent_payload(
            interaction_mode="both",
            tool_refs=["calculator"],
            model="gpt-example",
            limits={"timeout": 20, "max_steps": 3},
        ),
    )

    assert response.status_code == 200
    body = response.json()
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
    client = TestClient(registry.app)

    response = client.post(
        "/agents",
        json=agent_payload(interaction_mode="background-daemon"),
    )

    assert response.status_code == 422
