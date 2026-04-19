import json
import os
import time
from typing import Any

import requests

REGISTRY_URL = os.getenv("REGISTRY_URL", "http://localhost:8000").rstrip("/")
READER_URL = os.getenv("READER_URL", "http://localhost:8001").rstrip("/")
MATH_URL = os.getenv("MATH_URL", "http://localhost:8002").rstrip("/")

DEMO_CSV = """region,sales,orders
A,100,4
B,80,3
C,120,5
"""


def request_json(method: str, url: str, **kwargs: Any) -> Any:
    response = requests.request(method, url, timeout=10, **kwargs)
    response.raise_for_status()
    return response.json()


def wait_for_service(name: str, base_url: str) -> None:
    for _ in range(30):
        try:
            request_json("GET", f"{base_url}/health")
            return
        except requests.RequestException:
            time.sleep(1)
    raise RuntimeError(f"{name} did not become healthy at {base_url}")


def register_agents() -> None:
    agents = [
        {
            "name": "reader-agent",
            "version": "0.1.0",
            "description": "Reads inline CSV text and returns a normalized table artifact.",
            "endpoint": READER_URL,
            "capabilities": ["read.tabular"],
            "interaction_mode": "callable",
            "system_prompt": "Parse inline CSV into a structured table artifact.",
            "input_schema": {
                "type": "csv_text",
                "description": "Inline CSV text with a header row.",
            },
            "output_schema": {
                "artifact_type": "table",
                "description": "Columns, rows, and row-count metadata.",
            },
            "tool_refs": [],
            "model": "none",
            "limits": {"timeout": 10, "max_steps": 1},
        },
        {
            "name": "math-agent",
            "version": "0.1.0",
            "description": "Computes basic numeric metrics from table artifacts.",
            "endpoint": MATH_URL,
            "capabilities": ["analyze.basic-math"],
            "interaction_mode": "callable",
            "system_prompt": "Analyze numeric columns in a table artifact.",
            "input_schema": {
                "artifact_type": "table",
                "description": "Structured table artifact from reader-agent.",
            },
            "output_schema": {
                "artifact_type": "analysis",
                "description": "Row count, numeric column metrics, and simple findings.",
            },
            "tool_refs": [],
            "model": "none",
            "limits": {"timeout": 10, "max_steps": 1},
        },
    ]
    for agent in agents:
        request_json("POST", f"{REGISTRY_URL}/agents", json=agent)


def find_agent(capability: str) -> dict[str, Any]:
    matches = request_json("GET", f"{REGISTRY_URL}/search", params={"capability": capability})
    if not matches:
        raise RuntimeError(f"No agent found for capability {capability}")
    return matches[0]


def main() -> None:
    wait_for_service("registry", REGISTRY_URL)
    wait_for_service("reader-agent", READER_URL)
    wait_for_service("math-agent", MATH_URL)

    register_agents()

    reader_agent = find_agent("read.tabular")
    table_artifact = request_json(
        "POST",
        f"{reader_agent['endpoint']}/invoke",
        json={"csv_text": DEMO_CSV},
    )

    math_agent = find_agent("analyze.basic-math")
    analysis_artifact = request_json(
        "POST",
        f"{math_agent['endpoint']}/invoke",
        json=table_artifact,
    )

    print("agentarium MVP demo complete")
    print(f"reader-agent endpoint: {reader_agent['endpoint']}")
    print(f"math-agent endpoint: {math_agent['endpoint']}")
    print("final analysis artifact:")
    print(json.dumps(analysis_artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
