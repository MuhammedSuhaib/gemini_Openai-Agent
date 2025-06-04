# Planting-agent

A conversational AI assistant focused on plant expertise, built with [Chainlit](https://github.com/Chainlit/chainlit) and [openai-agents](https://github.com/Chainlit/openai-agents).

## Features

- Chatbot agent specialized in planting advice (short replies)
- Uses Gemini API via OpenAI-compatible interface
- Chainlit UI for interactive chat

## Future Improvements 
- Will make it stateful
- add authentication 
- make LLM more powerful

## Requirements

- Python 3.13+
- [Chainlit](https://github.com/Chainlit/chainlit) >= 2.5.5
- [openai-agents](https://github.com/Chainlit/openai-agents) >= 0.0.17
- [python-dotenv](https://github.com/theskumar/python-dotenv) >= 1.1.0

## Running the App

Start the Chainlit server:

```sh
chainlit run main.py
```

Then open the provided local URL in your browser to chat with the planting expert agent.

## Project Structure

- `main.py` — Main entrypoint, defines the agent and Chainlit event handlers.
- `.chainlit/` — Chainlit configuration and translations.
- `pyproject.toml` — Project metadata and dependencies.
