from fastapi.testclient import TestClient

from conftest import load_app_module


def test_reader_agent_invoke_normalizes_inline_csv():
    reader_agent = load_app_module("reader_agent_app", "agents/reader-agent/app.py")
    client = TestClient(reader_agent.app)

    response = client.post(
        "/invoke",
        json={"csv_text": "region,sales\nA,100\nB,80\n"},
    )

    assert response.status_code == 200
    assert response.json() == {
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
    }
