import csv
from io import StringIO
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="reader-agent")


class ReaderRequest(BaseModel):
    csv_text: str = Field(min_length=1)


class TableArtifact(BaseModel):
    artifact_type: str = "table"
    columns: list[str]
    rows: list[dict[str, Any]]
    metadata: dict[str, Any]


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
    rows = [
        {column: coerce_value(row.get(column, "")) for column in columns}
        for row in reader
    ]
    return TableArtifact(
        columns=columns,
        rows=rows,
        metadata={"row_count": len(rows)},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke", response_model=TableArtifact)
def invoke(request: ReaderRequest) -> TableArtifact:
    return parse_csv(request.csv_text)
