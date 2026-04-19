from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="report-writer-agent")


class AnalysisArtifact(BaseModel):
    artifact_type: str
    metrics: dict[str, Any]
    findings: list[str]


class ReportSection(BaseModel):
    title: str
    content: str


class ReportArtifact(BaseModel):
    artifact_type: str = "report"
    summary: str
    sections: list[ReportSection]
    metadata: dict[str, Any] = Field(default_factory=dict)


def format_number(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def write_report(analysis: AnalysisArtifact) -> ReportArtifact:
    if analysis.artifact_type != "analysis":
        raise HTTPException(status_code=400, detail="artifact_type must be analysis")

    row_count = analysis.metrics.get("row_count", 0)
    numeric_columns = analysis.metrics.get("numeric_columns", {})

    summary = (
        f"Analyzed {row_count} rows across {len(numeric_columns)} numeric columns."
    )

    sections = [
        ReportSection(
            title="Key Findings",
            content=" ".join(analysis.findings) if analysis.findings else "No findings.",
        )
    ]

    for column, metrics in numeric_columns.items():
        sections.append(
            ReportSection(
                title=f"Column: {column}",
                content=(
                    f"count={format_number(metrics.get('count'))}, "
                    f"sum={format_number(metrics.get('sum'))}, "
                    f"average={format_number(metrics.get('average'))}, "
                    f"min={format_number(metrics.get('min'))}, "
                    f"max={format_number(metrics.get('max'))}"
                ),
            )
        )

    return ReportArtifact(
        summary=summary,
        sections=sections,
        metadata={
            "source_artifact_type": analysis.artifact_type,
            "row_count": row_count,
            "numeric_column_count": len(numeric_columns),
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=ReportArtifact)
def invoke(analysis: AnalysisArtifact) -> ReportArtifact:
    return write_report(analysis)
