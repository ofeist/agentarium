from numbers import Number
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="math-agent")


class TableArtifact(BaseModel):
    artifact_type: str
    columns: list[str]
    rows: list[dict[str, Any]]
    metadata: dict[str, Any] = Field(default_factory=dict)


class NumericMetrics(BaseModel):
    count: int
    sum: float
    average: float
    min: float
    max: float


class AnalysisArtifact(BaseModel):
    artifact_type: str = "analysis"
    metrics: dict[str, Any]
    findings: list[str]


def analyze_table(table: TableArtifact) -> AnalysisArtifact:
    if table.artifact_type != "table":
        raise HTTPException(status_code=400, detail="artifact_type must be table")

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

    return AnalysisArtifact(
        metrics={
            "row_count": len(table.rows),
            "numeric_columns": numeric_columns,
        },
        findings=findings,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=AnalysisArtifact)
def invoke(table: TableArtifact) -> AnalysisArtifact:
    return analyze_table(table)
