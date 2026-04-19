# Suggested Repository Structure

```text
agentarium/
  README.md
  docker-compose.yml
  .env.example
  docs/
    MVP_DESCRIPTION.md
    IDEA_DESCRIPTION.md
    REPO_STRUCTURE.md
  registry/
    app.py
    requirements.txt
    Dockerfile
    models.py
  agents/
    reader-agent/
      app.py
      requirements.txt
      Dockerfile
    math-agent/
      app.py
      requirements.txt
      Dockerfile
  orchestrator/
    run_demo.py
    requirements.txt
  sample-data/
    sales.csv
```

## Notes

- `registry/` is the metadata and search service.
- `agents/reader-agent/` parses CSV and emits a normalized artifact.
- `agents/math-agent/` consumes the artifact and computes a small summary.
- `orchestrator/run_demo.py` is the end-to-end demo entrypoint.
- `sample-data/` contains one tiny CSV file for testing.

## Optional next structure

If the project grows, likely next additions are:

```text
  agents/
    report-writer-agent/
  schemas/
    agent-record.schema.json
    artifact-table.schema.json
    artifact-analysis.schema.json
  tests/
    test_registry.py
    test_reader_agent.py
    test_math_agent.py
    test_demo_flow.py
```
