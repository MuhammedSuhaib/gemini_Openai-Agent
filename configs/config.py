# configs\config.py
from agents import OpenAIChatCompletionsModel,AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
external_client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"),base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
model_config = OpenAIChatCompletionsModel(model='gemini-2.5-flash',openai_client=external_client)
