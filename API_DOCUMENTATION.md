# FastAPI CrewAI Agent Integration

This application now provides both a Gradio interface for sentiment analysis and a FastAPI endpoint for CrewAI agent interactions.

## Quick Start

Run the application:
```bash
uv run python app.py
```

This will start both servers:
- **FastAPI Server**: http://localhost:8000
- **Gradio Interface**: http://localhost:7861

## API Endpoints

### 1. Agent Interaction
**POST** `/agent`

Send text commands to the CrewAI agent.

**Request Body:**
```json
{
  "text": "Hello, can you help me with something?"
}
```

**Response:**
```json
{
  "response": "Hello! I'm a text assistant. How can I help you today?",
  "status": "success"
}
```

### 2. Health Check
**GET** `/health`

Check the API service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "CrewAI Text Agent API"
}
```

### 3. API Information
**GET** `/`

Get information about available endpoints.

## Example Usage

### Using curl
```bash
# Test the agent endpoint
curl -X POST "http://localhost:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{"text": "Tell me a joke"}'

# Check health
curl "http://localhost:8000/health"
```

### Using Python requests
```python
import requests

# Send a command to the agent
response = requests.post(
    "http://localhost:8000/agent",
    json={"text": "What time is it?"}
)
print(response.json())
```

## Agent Capabilities

The agent can respond to various types of requests:

- **Greetings**: "Hello", "Hi", "Hey"
- **Help requests**: "Can you help me?", "I need assistance"
- **Thanks**: "Thank you", "Thanks"
- **Time/Date**: "What time is it?", "What's the date?"
- **Weather**: "What's the weather like?"
- **Jokes**: "Tell me a joke", "Something funny"
- **General text**: Provides sentiment analysis and general responses

## Gradio Interface

The original sentiment analysis functionality is preserved and accessible at:
http://localhost:7861

This provides a web interface for analyzing text sentiment using TextBlob.

## Error Handling

The API includes comprehensive error handling:
- Empty text validation (400 error)
- Internal server errors (500 error)
- Proper exception handling with fallback responses

## Development

### Dependencies
- FastAPI for REST API
- CrewAI for agent functionality  
- Gradio for web interface
- TextBlob for sentiment analysis
- Uvicorn for ASGI server

### Linting
```bash
uv run ruff check .
```

### Testing
The application includes test scripts for verification:
- Basic API functionality
- Edge cases and error handling
- Both interface integration
- Sentiment analysis preservation