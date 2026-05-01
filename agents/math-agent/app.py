from numbers import Number
from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="math-agent")


class TableMetadata(BaseModel):
    row_count: int = Field(ge=0)
    column_count: int = Field(ge=0)
    source_format: Literal["csv"] = "csv"


class TableArtifact(BaseModel):
    artifact_type: Literal["table"]
    columns: list[str] = Field(min_length=1)
    rows: list[dict[str, Any]]
    metadata: TableMetadata


class NumericMetrics(BaseModel):
    count: int
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
    artifact_type: Literal["analysis"] = "analysis"
    metrics: AnalysisMetrics
    findings: list[str]
    metadata: AnalysisMetadata


def analyze_table(table: TableArtifact) -> AnalysisArtifact:
    numeric_columns: dict[str, NumericMetrics] = {}
    for column in table.columns:
        values = [
            row[column]
            for row in table.rows
            if isinstance(row.get(column), Number) and not isinstance(row.get(column), bool)
        ]
        if not values:
            continue

        total = float(sum(values))
        numeric_columns[column] = NumericMetrics(
            count=len(values),
            sum=total,
            average=total / len(values),
            min=float(min(values)),
            max=float(max(values)),
        )

    findings = [
        f"Column {column} has average {metrics.average:g} across {metrics.count} numeric values."
        for column, metrics in numeric_columns.items()
    ]
    if not findings:
        findings.append("No numeric columns were found for analysis.")

    row_count = len(table.rows)
    return AnalysisArtifact(
        metrics=AnalysisMetrics(
            row_count=row_count,
            numeric_columns=numeric_columns,
        ),
        findings=findings,
        metadata=AnalysisMetadata(
            row_count=row_count,
            numeric_column_count=len(numeric_columns),
            finding_count=len(findings),
        ),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=AnalysisArtifact)
def invoke(table: TableArtifact) -> AnalysisArtifact:
    return analyze_table(table)
