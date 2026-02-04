import chainlit as cl
import os
from agents import set_tracing_export_api_key
from my_agents.triage_agent import initialize_triage_agent, get_welcome_message, validate_api_key
from configs.chainlit import handle_start, handle_message
from agents.run import RunConfig


# Initialize tracing globally
set_tracing_export_api_key(os.getenv('Tracing_key'))

# Validate API key on startup
validate_api_key()


@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""
    # Initialize chat history
    await handle_start()

    # Initialize the triage agent
    Triage_Agent = initialize_triage_agent()

    cl.user_session.set("agent", Triage_Agent)  # Store the agent in user session
    cl.user_session.set("config", RunConfig())  # Store default config in user session

    # Send welcome message to user
    await cl.Message(content=get_welcome_message()).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    from agents import Agent
    from agents.run import RunConfig
    from typing import cast

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    await handle_message(message, agent, config)