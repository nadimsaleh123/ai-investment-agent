import importlib
import sys
from pathlib import Path

import pytest

# Ensure the package root is on the path when running via pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inv_agent import orchestrator, memory


def test_orchestrator_initializes_without_crewai(tmp_path, monkeypatch):
    """Orchestrator should initialize even when crewai is missing.

    The MemoryManager writes to disk on initialization, so patch it to use the
    pytest-provided ``tmp_path`` to avoid polluting the repository.
    """

    # Pretend ``crewai`` is not installed regardless of the test environment
    monkeypatch.setattr(orchestrator, "Crew", object)

    original_init = memory.MemoryManager.__init__

    def patched_init(self, base_dir="memory"):
        original_init(self, base_dir=tmp_path)

    monkeypatch.setattr(memory.MemoryManager, "__init__", patched_init)

    orch = orchestrator.Orchestrator()
    assert orch.crew is None
