# LangGraph Projects - Langchain_2

## Overview

A minimal LangGraph example that exposes an `agent` graph defined in `app.py`. The project binds a Groq-based LLM (`langchain_groq.ChatGroq`) with tools and runs a local LangGraph development server.

## Features

- Demonstrates binding Python callables as tools to an LLM
- Shows message normalization for LangChain message objects
- Provides a LangGraph config in `langgraph.json` for local development

## Prerequisites

- Python 3.11 (use `major.minor` format in LangGraph config)
- virtualenv (recommended)
- `GROQ_API_KEY` set in a `.env` file for `langchain_groq`

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

- `langgraph.json` controls LangGraph behavior. Ensure the `python_version` field uses `major.minor` only (for example: `"3.11"`). Do NOT include the patch version (`3.11.3`).
- Put your `GROQ_API_KEY` in a `.env` file at the project root:

```
GROQ_API_KEY=your_api_key_here
```

## Running the project

Start the LangGraph dev server from the activated virtualenv:

```bash
langgraph dev
```

The graph id is `agent` and is loaded from `app.py` as configured in `langgraph.json`.

## Project structure

- `app.py` — defines the graph (`agent`), the LLM, and tools. It should bind tools with `llm.bind_tools(...)`, normalize incoming messages to LangChain message objects, and pass bound tools to `ToolNode`.
- `langgraph.json` — LangGraph config (graphs, env, python_version, dependencies).
- `.env` — environment variables.
- `requirements.txt` — Python dependencies.

## Troubleshooting

- Invalid Python version format error:
	- Symptom: "Invalid Python version format: 3.11.3. Use 'major.minor' format (e.g., '3.11')."
	- Fix: Edit `langgraph.json` and change `"python_version": "3.11.3"` to `"python_version": "3.11"`.

- Unsupported function / format error when loading tools:
	- Symptom: ValueError about unsupported function list or format.
	- Fix: Use the LLM's `bind_tools()` to create properly formatted tool bindings and pass those bound tools to `ToolNode`. Example:

```python
tools = [multiply, add, divide]
bound_tools = llm.bind_tools(tools)
graph.add_node("tools", ToolNode(bound_tools))
```

## Contributing

- Make changes, run `langgraph dev`, and open issues or PRs for suggestions.
