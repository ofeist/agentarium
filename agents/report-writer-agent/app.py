from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="report-writer-agent")


class NumericMetrics(BaseModel):
    count: int = Field(ge=0)
    sum: float
    average: float
    min: float
    max: float


class AnalysisMetrics(BaseModel):
    row_count: int = Field(ge=0)
    numeric_columns: dict[str, NumericMetrics] = Field(default_factory=dict)


class AnalysisMetadata(BaseModel):
    source_artifact_type: Literal["table"] = "table"
    row_count: int = Field(ge=0)
    numeric_column_count: int = Field(ge=0)
    finding_count: int = Field(ge=0)


class AnalysisArtifact(BaseModel):
    artifact_type: Literal["analysis"]
    metrics: AnalysisMetrics
    findings: list[str]
    metadata: AnalysisMetadata


class ReportSection(BaseModel):
    title: str
    content: str


class ReportMetadata(BaseModel):
    source_artifact_type: Literal["analysis"] = "analysis"
    row_count: int = Field(ge=0)
    numeric_column_count: int = Field(ge=0)
    section_count: int = Field(ge=0)


class ReportArtifact(BaseModel):
    artifact_type: Literal["report"] = "report"
    summary: str
    sections: list[ReportSection] = Field(min_length=1)
    metadata: ReportMetadata


def format_number(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def write_report(analysis: AnalysisArtifact) -> ReportArtifact:
    row_count = analysis.metrics.row_count
    numeric_columns = analysis.metrics.numeric_columns
    numeric_column_count = len(numeric_columns)

    summary = (
        f"Analyzed {row_count} rows across {numeric_column_count} numeric columns."
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
                    f"count={format_number(metrics.count)}, "
                    f"sum={format_number(metrics.sum)}, "
                    f"average={format_number(metrics.average)}, "
                    f"min={format_number(metrics.min)}, "
                    f"max={format_number(metrics.max)}"
                ),
            )
        )

    return ReportArtifact(
        summary=summary,
        sections=sections,
        metadata=ReportMetadata(
            row_count=row_count,
            numeric_column_count=numeric_column_count,
            section_count=len(sections),
        ),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=ReportArtifact)
def invoke(analysis: AnalysisArtifact) -> ReportArtifact:
    return write_report(analysis)
