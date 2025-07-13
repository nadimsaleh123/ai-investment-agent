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


def test_route_request_invokes_kickoff(monkeypatch):
    """route_request should use CrewAI's kickoff when available."""
    from inv_agent.orchestrator import Orchestrator

    orch = Orchestrator()
    agent = orch.agents["gold"]

    called = {}

    def fake_kickoff(prompt):
        called["prompt"] = prompt

        class Out:
            def __str__(self):
                return "OK"

        return Out()

    monkeypatch.setattr(agent.__class__, "kickoff", lambda self, prompt: fake_kickoff(prompt))
    if hasattr(agent, "run"):
        monkeypatch.delattr(agent.__class__, "run", raising=False)

    result = orch.route_request("gold", "brief")

    assert result == "OK"
    assert "brief" in called["prompt"]
