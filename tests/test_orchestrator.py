import importlib
import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inv_agent.orchestrator import Orchestrator


def test_orchestrator_initializes_without_crewai(tmp_path, monkeypatch):
    """Ensure orchestrator can initialize without CrewAI installed."""
    # Simulate crewai being absent even if it exists in the environment
    original_find_spec = importlib.util.find_spec

    def fake_find_spec(name, *args, **kwargs):
        if name == "crewai":
            return None
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)
    monkeypatch.setattr("inv_agent.orchestrator.Crew", object)

    crewai = importlib.util.find_spec("crewai")
    assert crewai is None

    from inv_agent.memory import MemoryManager

    class TmpMemoryManager(MemoryManager):
        def __init__(self):
            super().__init__(base_dir=tmp_path)

    monkeypatch.setattr("inv_agent.orchestrator.MemoryManager", TmpMemoryManager)

    orch = Orchestrator()
    assert orch.crew is None
    assert orch.memory.base_path == tmp_path
