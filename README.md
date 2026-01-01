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

## Deploying on Hugging Face Spaces

This application is ready to be deployed on Hugging Face Spaces using Docker. The necessary Dockerfile and configuration files are included in the repository.

To deploy:
1. Create a new Space on Hugging Face
2. Select "Docker" as the SDK
3. Configure the environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `OAUTH_GITHUB_CLIENT_ID`: GitHub OAuth client ID (optional)
   - `OAUTH_GITHUB_CLIENT_SECRET`: GitHub OAuth client secret (optional)
4. The application will be automatically built and deployed

### Automated Deployment with GitHub Actions

This repository includes a GitHub Actions workflow for automated deployment to Hugging Face Spaces. To use it:

1. Add the following secrets to your GitHub repository:
   - `HF_TOKEN`: Your Hugging Face access token (with write permissions)
   - `HF_SPACE_ID`: Your Space ID in the format `username/space-name`

2. The workflow will automatically deploy to your Space when you push to the `main` branch.

The workflow file is located at `.github/workflows/deploy.yml`.
