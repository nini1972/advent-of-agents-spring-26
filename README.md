# Advent of Agents (Spring 2026)

This repository contains the code for various agents (Fanout, Sculptor, Critic, Hierarchical) built using the Google Agent Development Kit (ADK).

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (Python package and environment manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aoa-luissala
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

## Environment Setup

You need a Google Gemini API key to run these agents.

1. Get an API key from [Google AI Studio](https://aistudio.google.com/).
2. Copy the sample environment file:
   ```bash
   cp sample.env .env
   ```
3. Edit the `.env` file and replace `"your_api_key_here"` with your actual API key.

*Note: The `.env` file is ignored by Git to keep your API keys secure.*

## Running the Agents

There are two main ways to execute the agents:

### 1. Locally via Command Line
You can run any specific agent directly. For example, to run the Hierarchical agent:
```bash
uv run python agents/hierarchical/agent.py
```
This will start an interactive runner where you can enter prompts directly in your terminal.

### 2. Via the ADK Web UI
If you prefer a visual interface, you can launch the built-in ADK web experience:
```bash
uv run adk web agents --port 21000
```
Then, open your browser and navigate to `http://localhost:21000/dev-ui/` to interact with all the deployed Apps.
