# ai-investment-agent

This project implements a proof-of-concept multi-agent investment advisor using [CrewAI](https://github.com/joaomdmoura/crewAI) with a simple Gradio front end.

## Features

- Specialized analysis agents for different markets (gold, silver, oil & gas, renewable energy, chip manufacturing and AI companies).
- An orchestrator that routes daily briefs to the relevant agent and stores the history of briefs.
- A Python coder agent is included for future automation tasks.

## Running

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the Gradio interface:
   ```bash
   python -m inv_agent.frontend
   ```

CrewAI is required for the agents to function. If it is not installed, placeholder messages will be returned.
