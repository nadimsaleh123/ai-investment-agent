from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
import os

MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

try:
    from crewai import Agent
except ImportError:  # pragma: no cover - library not installed

    class Agent:  # type: ignore
        """Fallback agent used when crewAI is unavailable."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
            """Initialize a dummy agent that ignores all parameters."""

        def run(self, prompt: str) -> str:
            return "[crewAI not installed]"


def create_analysis_agent(name: str, description: str) -> Agent:
    """Factory for creating a CrewAI agent specialized in an asset class."""
    return Agent(
        role="analyst",
        goal="Analyze asset history and daily briefs to advise on investments.",
        backstory=description,
        allow_delegation=False,
        verbose=True,
        llm=MODEL_NAME,
    )


def create_python_coder_agent() -> Agent:
    """Agent that can write Python code."""
    return Agent(
        role="engineer",
        goal="Write Python code and build a user interface.",
        backstory="An expert Python developer helping with tools and front end.",
        allow_delegation=False,
        verbose=True,
        llm=MODEL_NAME,
    )


def build_agents() -> Dict[str, Agent]:
    """Create all domain agents and return them in a dict."""
    descriptions = {
        "gold": "Expert in gold market trends and company performance.",
        "silver": "Expert in silver market trends and company performance.",
        "o&g": "Expert in public oil and gas companies.",
        "renewable energy": "Expert in public renewable energy companies.",
        "chip manufacturing": "Expert in public chip manufacturing companies.",
        "ai companies": "Expert in public AI company performance.",
    }
    agents = {
        name: create_analysis_agent(name, desc) for name, desc in descriptions.items()
    }
    agents["python_coder"] = create_python_coder_agent()
    return agents
