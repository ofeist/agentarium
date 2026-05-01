import csv
from io import StringIO
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="reader-agent")


class ReaderRequest(BaseModel):
    csv_text: str = Field(min_length=1)


class TableMetadata(BaseModel):
    row_count: int = Field(ge=0)
    column_count: int = Field(ge=0)
    source_format: Literal["csv"] = "csv"


class TableArtifact(BaseModel):
    artifact_type: Literal["table"] = "table"
    columns: list[str] = Field(min_length=1)
    rows: list[dict[str, Any]]
    metadata: TableMetadata


def coerce_value(value: str) -> Any:
    stripped = value.strip()
    if stripped == "":
        return ""
    try:
        return int(stripped)
    except ValueError:
        pass
    try:
        return float(stripped)
    except ValueError:
        return stripped


def parse_csv(csv_text: str) -> TableArtifact:
    reader = csv.DictReader(StringIO(csv_text.strip()))
    columns = reader.fieldnames or []
    if not columns:
        raise HTTPException(status_code=400, detail="csv_text must include a header row")

    rows = [
        {column: coerce_value(row.get(column, "")) for column in columns}
        for row in reader
    ]
    return TableArtifact(
        columns=columns,
        rows=rows,
        metadata=TableMetadata(
            row_count=len(rows),
            column_count=len(columns),
        ),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=TableArtifact)
def invoke(request: ReaderRequest) -> TableArtifact:
    return parse_csv(request.csv_text)
