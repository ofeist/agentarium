from pathlib import Path

import yaml

from conftest import load_app_module


ROOT = Path(__file__).resolve().parents[1]
AGENT_METADATA_DIR = ROOT / "registry" / "agents"
EXPECTED_FIELDS = {
    "name",
    "version",
    "description",
    "endpoint",
    "capabilities",
    "interaction_mode",
    "runtime_type",
    "system_prompt",
    "input_schema",
    "output_schema",
    "tool_refs",
    "model",
    "limits",
}
EXPECTED_FILES = {
    "reader-agent.yaml",
    "math-agent.yaml",
    "report-writer-agent.yaml",
}


def test_agent_metadata_files_match_live_registry_model():
    registry = load_app_module("registry_app_agent_metadata", "registry/app.py")
    paths = sorted(AGENT_METADATA_DIR.glob("*.yaml"))

    assert {path.name for path in paths} == EXPECTED_FILES

    for path in paths:
        data = yaml.safe_load(path.read_text())
        assert set(data) == EXPECTED_FIELDS

        record = registry.AgentRegistration(**data)
        body = record.model_dump(mode="json")

        assert body["runtime_type"] == "packaged-agent"
        assert body["interaction_mode"] == "callable"
