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


def test_generate_report(monkeypatch):
    """generate_report should return a string even if requests fail."""
    from inv_agent.orchestrator import Orchestrator

    orch = Orchestrator()

    class DummyResp:
        def json(self):
            return {}

    monkeypatch.setattr("requests.post", lambda *a, **k: DummyResp())

    report = orch.generate_report()
    assert isinstance(report, str)
