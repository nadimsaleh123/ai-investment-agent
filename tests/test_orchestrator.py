import importlib
import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inv_agent.orchestrator import Orchestrator


def test_orchestrator_initializes_without_crewai():
    """Initialize orchestrator when crewai is not installed."""
    crewai_spec = importlib.util.find_spec("crewai")
    if crewai_spec is not None:
        pytest.skip("crewai is installed")
    orch = Orchestrator()
    assert orch.crew is None
