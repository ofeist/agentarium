from conftest import load_app_module


def test_reader_agent_invoke_normalizes_inline_csv():
    reader_agent = load_app_module("reader_agent_app", "agents/reader-agent/app.py")
    response = reader_agent.invoke(
        reader_agent.ReaderRequest(csv_text="region,sales\nA,100\nB,80\n")
    )

    assert response.model_dump(mode="json") == {
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
