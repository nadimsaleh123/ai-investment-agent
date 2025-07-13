from __future__ import annotations

from typing import Dict, List

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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
        # The agent run method is part of CrewAI; we assume it returns a string.
        try:
            response = agent.run(prompt)  # type: ignore[attr-defined]
        except AttributeError:
            response = "[crewAI not installed]"
        self.memory.append_entry(asset, brief)
        return response
