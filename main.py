import chainlit as cl
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
#                                   ⬆               ⬆
#                                 Just bcz i m using gemini
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=provider
)

agent = Agent(
    name='1st_Agent',
    instructions='you are expert in planting but only short replies',
    model=model
)


# chainlit decorator for when a new chat session starts
@cl.on_chat_start
async def handle_chat_start():
    # Send welcome message to user
    await cl.Message(content="Hello! I am a planting expert").send()

# chainlit decorator for when a new message is received
@cl.on_message
async def handle_message(message: cl.Message):
    # Get the message content from user
    prompt = message.content
    output = Runner.run_sync(starting_agent=agent, input=prompt)
    await cl.Message(output.final_output).send()