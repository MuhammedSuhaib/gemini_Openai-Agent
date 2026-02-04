import chainlit as cl
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
#                                   ⬆               ⬆
#                                 Just bcz i m using gemini
from agents.run import RunConfig
from dotenv import load_dotenv
load_dotenv()
from configs.config import model_config
from typing import cast  # Type hints for better code clarity
from colorama import Fore
from agents.agents import MuhammadSuhaibAssistant, SocialMediaPoster
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# Check if the API key is present; if not, raise an error
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():

    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
# Triage Agent — routes to correct custom agent

    Triage_Agent = Agent(
        name="Triage_Agent",
        instructions="""
        Decide which specialist should handle the request.

        Routing rules:
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


    cl.user_session.set("agent", Triage_Agent)  # Store the agent in user session
    cl.user_session.set("config", RunConfig())  # Store default config in user session

    # Send welcome message to user
    await cl.Message(content="👋 Hi!  I'm your Social Media Post Agent. Ready to help you plan and post engaging content about your tech journey—Python, JS/TS, Next.js, AI & more. Let's grow your presence with smart, hashtag-optimized posts!").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print( "\n \t \t \t  CALLING_AGENT_WITH_CONTEXT\n", Fore.YELLOW + str(history) + "\n" + Fore.RESET)

        output = Runner.run_streamed(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        async for events in output.stream_events():
            if events.type == 'raw_response_event' and hasattr(events.data, "delta"):
                msg.content += events.data.delta
                await msg.update()
        
        # Update the session with the new history.
        cl.user_session.set("chat_history", output.to_input_list())
        
        # Optional: Log the interaction
        print(Fore.CYAN + f"User: {message.content} " + Fore.RESET)
        print(Fore.LIGHTGREEN_EX + f"Assistant: {msg.content}" + Fore.RESET)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")