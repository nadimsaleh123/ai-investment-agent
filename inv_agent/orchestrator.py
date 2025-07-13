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
    Crew = None  # type: ignore

from .agents import build_agents
from .memory import MemoryManager


class Orchestrator:
    def __init__(self):
        self.agents = build_agents()
        self.memory = MemoryManager()
        if Crew is None:
            # CrewAI isn't installed; skip crew creation to avoid TypeError
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
        try:
            result = agent.kickoff(prompt)  # type: ignore[attr-defined]
            response = getattr(result, "raw", str(result))
        except AttributeError:
            response = "[crewAI not installed]"
        except Exception:
            response = "[execution failed]"
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
                res_obj = agent.kickoff(prompt)  # type: ignore[attr-defined]
                result = getattr(res_obj, "raw", str(res_obj))
            except AttributeError:
                result = "[crewAI not installed]"
            except Exception:
                result = "[execution failed]"
            sections.append(f"## {name}\n{result}")

        return "\n\n".join(sections)
