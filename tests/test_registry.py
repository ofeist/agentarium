from fastapi.testclient import TestClient

from conftest import load_app_module


def test_registry_search_returns_matching_agents_by_capability():
    registry = load_app_module("registry_app", "registry/app.py")
    registry.AGENTS.clear()
    client = TestClient(registry.app)

    client.post(
        "/agents",
        json={
            "name": "reader-agent",
            "version": "0.1.0",
            "endpoint": "http://reader-agent:8001",
            "capabilities": ["read.tabular"],
        },
    ).raise_for_status()
    client.post(
        "/agents",
        json={
            "name": "math-agent",
            "version": "0.1.0",
            "endpoint": "http://math-agent:8002",
            "capabilities": ["analyze.basic-math"],
        },
    ).raise_for_status()

    response = client.get("/search", params={"capability": "read.tabular"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "reader-agent",
            "version": "0.1.0",
            "endpoint": "http://reader-agent:8001",
            "capabilities": ["read.tabular"],
        }
    ]
