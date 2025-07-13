from __future__ import annotations

from typing import Dict, List

import requests

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

    def generate_report(self) -> str:
        """Compile analysis from all agents using Serper search results."""
        if not SERPER_API_KEY:
            return "[Serper API key not configured]"

        sections: List[str] = []
        for name, agent in self.agents.items():
            if name == "python_coder":
                continue
            try:
                resp = requests.post(
                    "https://google.serper.dev/news",
                    headers={"X-API-KEY": SERPER_API_KEY},
                    json={"q": name, "num": 3},
                    timeout=10,
                )
                data = resp.json()
                snippets = []
                for item in data.get("news", []):
                    title = item.get("title", "")
                    link = item.get("link", "")
                    snippets.append(f"{title} - {link}")
                research = " ".join(snippets) if snippets else "No results"
            except Exception:
                research = "[search failed]"

            history = self.memory.get_history(name)
            prompt = (
                f"Research findings: {research}. "
                f"Historical briefs: {history}. "
                f"Provide your investment view on {name}."
            )
            try:
                result = agent.run(prompt)  # type: ignore[attr-defined]
            except AttributeError:
                result = "[crewAI not installed]"
            sections.append(f"## {name}\n{result}")

        return "\n\n".join(sections)
