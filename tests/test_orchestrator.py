import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inv_agent.orchestrator import Orchestrator
from inv_agent.memory import MemoryManager
import json


def test_orchestrator_initializes_without_crewai(monkeypatch):
    """Orchestrator should skip crew creation when CrewAI is patched out."""
    monkeypatch.setattr("inv_agent.orchestrator.Crew", object)
    orch = Orchestrator()
    assert orch.crew is None


def test_route_request_appends_history(monkeypatch, tmp_path):
    """route_request should write the brief to memory and return placeholder."""
    monkeypatch.setattr("inv_agent.orchestrator.Crew", object)
    orch = Orchestrator()
    orch.memory = MemoryManager(base_dir=tmp_path)

    asset = "gold"
    brief = "Sample brief for testing"
    response = orch.route_request(asset, brief)

    assert response == "[crewAI not installed]"

    file_path = orch.memory._file_for_asset(asset)
    assert file_path.exists()
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == [brief]
    assert orch.memory.get_history(asset) == [brief]
