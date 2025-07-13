import importlib
import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_orchestrator_initializes_without_crewai(monkeypatch):
    """Orchestrator should handle missing crewai dependency."""
    if importlib.util.find_spec("crewai") is not None:
        pytest.skip("crewai is installed")
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None)
    from inv_agent.orchestrator import Orchestrator

    orch = Orchestrator()
    assert orch.crew is None
