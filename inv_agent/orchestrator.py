from __future__ import annotations

from typing import Dict, List

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

try:
    from crewai import Crew
except ImportError:  # pragma: no cover - library not installed
    Crew = object  # type: ignore

from .agents import build_agents
from .memory import MemoryManager


class Orchestrator:
    def __init__(self):
        self.agents = build_agents()
        self.memory = MemoryManager()
        if Crew is object:
            # crewAI isn't installed; skip crew creation to avoid TypeError
            self.crew = None
        else:
            self.crew = Crew(agents=list(self.agents.values()))  # type: ignore

    def route_request(self, asset: str, brief: str) -> str:
        """Send the daily brief to the appropriate agent and return the response."""
        if asset not in self.agents:
            raise ValueError(f"No agent found for asset {asset}")
        agent = self.agents[asset]
        history = self.memory.get_history(asset)
        prompt = (
            "You are analyzing the following asset: "
            f"{asset}. Here is the historical context: {history}."
            f" Daily brief: {brief}. Provide investment advice based on cause and "
            "effect patterns."
        )
        # Execute the agent using CrewAI if available. Older versions exposed a
        # ``run`` method while newer releases use ``kickoff`` which returns a
        # ``LiteAgentOutput`` object. We support both to remain backwards
        # compatible.
        try:
            if hasattr(agent, "run"):
                response = agent.run(prompt)  # type: ignore[attr-defined]
            else:
                result = agent.kickoff(prompt)  # type: ignore[attr-defined]
                response = str(result)
        except AttributeError:
            # crewAI isn't installed; fall back to placeholder response
            response = "[crewAI not installed]"
        except Exception as exc:  # pragma: no cover - runtime issues
            # Surface the underlying error so the caller can troubleshoot
            response = f"[error: {exc}]"
        self.memory.append_entry(asset, brief)
        return response
