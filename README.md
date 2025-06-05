# SocialMediaScheduler Agent

A Chainlit-based AI agent that plans and schedules engaging LinkedIn and Twitter posts focused on tech learning (Python, JS/TS, Next.js, AI, etc.).

## Features

* Uses Gemini API for AI completions
* Creates concise, professional posts with relevant hashtags and tags
* Engages tech community and learners with trend-aware content

## Setup

1. Install dependencies (Chainlit, dotenv, your AI agent code).
2. Add your Gemini API key to a `.env` file:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the Chainlit app.

## Usage

Start a chat, send your prompt about social media scheduling, and get AI-generated post suggestions optimized with hashtags and tags.

---

## Future Improvements 
- Make it stateful
- Add authentication 
- Make LLM more powerful

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

Then open the provided local URL in your browser to chat with the agent.

## Project Structure

- `main.py` — Main entrypoint, defines the agent and Chainlit event handlers.
- `.chainlit/` — Chainlit configuration and translations.
- `pyproject.toml` — Project metadata and dependencies.

