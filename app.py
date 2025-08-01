import json
import threading

import gradio as gr
import uvicorn
from crewai import Agent, Crew, Task
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob


def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        str: A JSON string containing polarity, subjectivity, and assessment
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment

    result = {
        "polarity": round(sentiment.polarity, 2),  # -1 (negative) to 1 (positive)
        "subjectivity": round(
            sentiment.subjectivity, 2
        ),  # 0 (objective) to 1 (subjective)
        "assessment": "positive"
        if sentiment.polarity > 0
        else "negative"
        if sentiment.polarity < 0
        else "neutral",
    }

    return json.dumps(result)


# FastAPI Models
class AgentCommand(BaseModel):
    text: str


class AgentResponse(BaseModel):
    response: str
    status: str


# CrewAI Agent Setup
def create_crew_agent():
    """Create a CrewAI agent for processing text commands."""
    agent = Agent(
        role="Text Assistant",
        goal="Help users by analyzing and responding to their text commands",
        backstory="""You are a helpful text assistant that can understand and 
        respond to various text-based requests. You analyze the input and provide 
        meaningful, helpful responses based on the command given.""",
        verbose=True,
        allow_delegation=False,
        max_iter=1,
        llm="ollama/llama2",  # Use local Ollama model, fallback if not available
    )
    return agent


def process_agent_command(text: str) -> str:
    """Process a text command using CrewAI agent."""
    try:
        # Create agent and task
        agent = create_crew_agent()
        
        task = Task(
            description=f"Analyze and respond to this command: {text}",
            expected_output="A helpful and informative response to the user's command",
            agent=agent,
        )
        
        # Create crew and execute
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        
        return str(result)
    except Exception:
        # Fallback to a simple response if CrewAI fails
        return create_simple_response(text)


def create_simple_response(text: str) -> str:
    """Create a simple response when CrewAI is not available."""
    text_lower = text.lower().strip()
    
    # Simple pattern matching for common requests (order matters)
    if any(word in text_lower for word in ["thank", "thanks"]):
        return (
            "You're welcome! I'm glad I could help. "
            "Is there anything else you'd like to know?"
        )
    
    elif any(word in text_lower for word in ["help", "assist", "support"]):
        return (
            "I'm here to help! I can respond to various text commands, "
            "analyze sentiment, and provide information. What would you like to know?"
        )
    
    elif any(greeting in text_lower for greeting in ["hello", "hi", "hey"]):
        return "Hello! I'm a text assistant. How can I help you today?"
    
    elif any(word in text_lower for word in ["weather", "temperature"]):
        return (
            "I'm sorry, I don't have access to real-time weather data. "
            "Please check a weather website or app for current conditions."
        )
    
    elif any(word in text_lower for word in ["joke", "funny", "laugh"]):
        return (
            "Here's a programming joke for you: Why do programmers prefer dark mode? "
            "Because light attracts bugs! 🐛"
        )
    
    elif any(word in text_lower for word in ["time", "date"]):
        return (
            "I don't have access to real-time information, but you can check "
            "the current time and date on your device."
        )
    
    else:
        # Analyze the text and provide a general response
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        response = f"I received your message: '{text}'. "
        
        if sentiment.polarity > 0.1:
            response += "I notice your message has a positive tone! "
        elif sentiment.polarity < -0.1:
            response += "I notice your message has a negative tone. "
        else:
            response += "Your message seems neutral. "
        
        response += (
            "While I'd love to help more specifically, I can provide general "
            "assistance, answer questions, or just chat. What would you like to do?"
        )
        
        return response


# FastAPI App
app = FastAPI(title="CrewAI Text Agent API", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CrewAI Text Agent API",
        "endpoints": {
            "POST /agent": "Send text commands to the CrewAI agent",
            "GET /health": "Health check endpoint",
        },
        "gradio_interface": "http://localhost:7861",
    }


@app.post("/agent", response_model=AgentResponse)
async def process_command(command: AgentCommand) -> AgentResponse:
    """
    Process a text command using the CrewAI agent.
    
    Args:
        command: AgentCommand with text field
        
    Returns:
        AgentResponse with the agent's response
    """
    try:
        if not command.text.strip():
            raise HTTPException(status_code=400, detail="Text command cannot be empty")
        
        response = process_agent_command(command.text)
        return AgentResponse(response=response, status="success")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "CrewAI Text Agent API"}


# Create the Gradio interface
demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(placeholder="Enter text to analyze..."),
    outputs=gr.Textbox(),  # Changed from gr.JSON() to gr.Textbox()
    title="Text Sentiment Analysis",
    description="Analyze the sentiment of text using TextBlob",
)


def run_fastapi():
    """Run FastAPI server."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


def run_gradio():
    """Run Gradio interface."""
    demo.launch(server_name="0.0.0.0", server_port=7861)


# Launch both interfaces
if __name__ == "__main__":
    print("Starting both FastAPI and Gradio servers...")
    print("FastAPI will be available at: http://localhost:8000")
    print("Gradio interface will be available at: http://localhost:7861")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Run Gradio in the main thread
    run_gradio()
