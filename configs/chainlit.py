import chainlit as cl
from agents import Agent, Runner, trace
from agents.run import RunConfig
from colorama import Fore


async def handle_start():
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])


async def handle_message(message: cl.Message, agent: Agent, config: RunConfig):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="")
    await msg.send()

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    # Use the session ID for tracing group_id
    session_id = cl.user_session.get("id", "chainlit-session")

    try:
        print("\n \t \t \t  CALLING_AGENT_WITH_CONTEXT\n", Fore.YELLOW + str(history) + "\n" + Fore.RESET)

        # Wrap the execution in a trace block
        with trace(workflow_name="Chainlit Social Media Assistant", group_id=str(session_id)):
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