import chainlit as cl
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
#                                   ⬆               ⬆
#                                 Just bcz i m using gemini
from agents.run import RunConfig
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
    name='colored',
    instructions="I m trying to get cool responses from you , like colored outputs etc give me your best shot using the power of md in m viewing your reponses on chainlit ui  without code blocks , But always reply in the shortest way possible ",
    model=model
)


@cl.on_message
async def handle_message(message: cl.Message):
    # Get the message content from user
    prompt = message.content
    output = Runner.run_sync(starting_agent=agent, input=prompt ,run_config=RunConfig(tracing_disabled=True))
    await cl.Message(output.final_output).send()
