import importlib
import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inv_agent.orchestrator import Orchestrator


def test_orchestrator_initializes_without_crewai():
    # Ensure crewai is really not available for this test
    crewai = importlib.util.find_spec("crewai")
    assert crewai is None
    orch = Orchestrator()
    assert orch.crew is None
