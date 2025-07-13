# ai-investment-agent

This project implements a proof-of-concept multi-agent investment advisor using [CrewAI](https://github.com/joaomdmoura/crewAI) with a polished Gradio front end.

## Features

- Specialized analysis agents for different markets (gold, silver, oil & gas, renewable energy, chip manufacturing and AI companies).
- An orchestrator that routes daily briefs to the relevant agent and stores the history of briefs.
- A Python coder agent is included for future automation tasks.
- Enhanced Gradio interface with improved layout and theming.
- Generate consolidated reports using Serper research across all assets.

## Running

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the Gradio interface:
   ```bash
   python -m inv_agent.frontend
   ```

### Model configuration

All agents default to OpenAI's `gpt-4o-mini` model. You can override this by
setting the `OPENAI_MODEL_NAME` environment variable in your `.env` file.

CrewAI is required for the agents to function. If it is not installed, placeholder messages will be returned.
