import pytest
from pydantic import ValidationError

from conftest import load_app_module


def test_report_writer_agent_formats_analysis_artifact():
    report_writer_agent = load_app_module(
        "report_writer_agent_app",
        "agents/report-writer-agent/app.py",
    )

    response = report_writer_agent.invoke(
        report_writer_agent.AnalysisArtifact(
            artifact_type="analysis",
            metrics={
                "row_count": 3,
                "numeric_columns": {
                    "sales": {
                        "count": 3,
                        "sum": 300.0,
                        "average": 100.0,
                        "min": 80.0,
                        "max": 120.0,
                    }
                },
            },
            findings=[
                "Column sales has average 100 across 3 numeric values."
            ],
            metadata={
                "source_artifact_type": "table",
                "row_count": 3,
                "numeric_column_count": 1,
                "finding_count": 1,
            },
        )
    )

    assert response.model_dump(mode="json") == {
        "artifact_type": "report",
        "summary": "Analyzed 3 rows across 1 numeric columns.",
        "sections": [
            {
                "title": "Key Findings",
                "content": "Column sales has average 100 across 3 numeric values.",
            },
            {
                "title": "Column: sales",
                "content": "count=3, sum=300, average=100, min=80, max=120",
            },
        ],
        "metadata": {
            "source_artifact_type": "analysis",
            "row_count": 3,
            "numeric_column_count": 1,
            "section_count": 2,
        },
    }


def test_report_writer_agent_rejects_non_analysis_artifact():
    report_writer_agent = load_app_module(
        "report_writer_agent_app_invalid",
        "agents/report-writer-agent/app.py",
    )

    with pytest.raises(ValidationError):
        report_writer_agent.AnalysisArtifact(
            artifact_type="table",
            metrics={"row_count": 0, "numeric_columns": {}},
            findings=[],
            metadata={
                "source_artifact_type": "table",
                "row_count": 0,
                "numeric_column_count": 0,
                "finding_count": 0,
            },
        )
