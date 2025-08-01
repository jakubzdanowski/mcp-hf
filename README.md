# mcp-hf

A multi-interface application providing both sentiment analysis via Gradio and CrewAI agent interactions via FastAPI.

## Features

- **FastAPI REST API**: CrewAI agent endpoint for text command processing
- **Gradio Web Interface**: Interactive sentiment analysis using TextBlob  
- **Dual Server Setup**: Both interfaces run concurrently
- **MCP Integration**: Model Context Protocol support for agent interactions

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Run the application:
```bash
uv run python app.py
```

3. Access the interfaces:
- **FastAPI API**: http://localhost:8000
- **Gradio Interface**: http://localhost:7861

## API Usage

Send POST requests to `/agent` with text commands:

```bash
curl -X POST "http://localhost:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, can you help me?"}'
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API details.

## Development

- **Linting**: `uv run ruff check .`
- **Dependencies**: Managed with uv package manager
- **Python Version**: 3.13+