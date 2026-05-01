from fastapi.testclient import TestClient

from conftest import load_app_module


def test_math_agent_invoke_computes_basic_numeric_metrics():
    math_agent = load_app_module("math_agent_app", "agents/math-agent/app.py")
    client = TestClient(math_agent.app)

    response = client.post(
        "/invoke",
        json={
            "artifact_type": "table",
            "columns": ["region", "sales"],
            "rows": [
                {"region": "A", "sales": 100},
                {"region": "B", "sales": 80},
            ],
            "metadata": {
                "row_count": 2,
                "column_count": 2,
                "source_format": "csv",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["artifact_type"] == "analysis"
    assert body["metrics"]["row_count"] == 2
    assert body["metrics"]["numeric_columns"]["sales"] == {
        "count": 2,
        "sum": 180.0,
        "average": 90.0,
        "min": 80.0,
        "max": 100.0,
    }
    assert body["findings"] == [
        "Column sales has average 90 across 2 numeric values."
    ]
    assert body["metadata"] == {
        "source_artifact_type": "table",
        "row_count": 2,
        "numeric_column_count": 1,
        "finding_count": 1,
    }
