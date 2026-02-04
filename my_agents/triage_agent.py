import os
from agents import Agent
from configs.config import model_config
from my_agents.agents import MuhammadSuhaibAssistant, SocialMediaPoster


def initialize_triage_agent():
    """Initialize the Triage Agent that routes to correct specialists."""
    return Agent(
        name="Triage_Agent",
        instructions="""
        Decide which specialist should handle the request.

        Routing rules:
        -Always start by greeting the user and asking their intent.
        - If the query is about Muhammad Suhaib, his profile, career, skills, or projects → handoff to MuhammadSuhaibAssistant.
        - If the user explicitly asks for a LinkedIn or Twitter post → handoff to SocialMediaPoster.
        - Otherwise, respond that no suitable agent is available.
        """,
        model=model_config,
        handoffs=[
            MuhammadSuhaibAssistant,
            SocialMediaPoster
        ]
    )


def get_welcome_message():
    """Return the welcome message for the chat."""
    return "👋 Hi! I'm your AI assistant for Muhammad Suhaib's professional profile and social media content. I can help you learn about Suhaib's background, skills, and projects, or create engaging social media posts. How can I assist you today?"


def validate_api_key():
    """Validate that required API keys are set."""
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

    return GEMINI_API_KEY