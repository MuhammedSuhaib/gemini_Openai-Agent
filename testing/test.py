# test.py
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

agent = Agent(
    name="SocialMediaPoster",
    instructions="write social media posts about technology",
    model=model
)

config = RunConfig()
chat_history = []


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
async def chat(data: ChatIn):
    chat_history.append({"role": "user", "content": data.message})

    async def stream():
        output = Runner.run_streamed(
            starting_agent=agent,
            input=chat_history,
            run_config=config
        )

        async for event in output.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                yield event.data.delta

        chat_history[:] = output.to_input_list()

    return StreamingResponse(stream(), media_type="text/plain")
