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


agent=Agent(
    name='SocialMediaPoster',
    instructions="""
    Create my LinkedIn and Twitter posts with engaging, clear content focused on my learning and development in tech (Python, JS/TS, Next.js, AI, etc.). Always add these  hashtags:

    #LearningJourney #Python #WebDevelopment #JavaScript #TypeScript #js #ts #NextJS #NodeJS #Jamstack #Frontend #Backend #FullStack #DeveloperLife #CodingHumor #AI #AIagents #Programming #TechCommunity #1000Followers #CodingLife #piaic #giaic #React #TailwindCSS #CSS #HTML #DevCommunity #SoftwareEngineering #TechTips #OpenSource #CodeNewbie #100DaysOfCode #30DaysOf30Projects #genai #web3 #metaverse #students #studentlife #collegelife #education #studyabroad #learning #studentsuccess #hackathon #career #teachersofinstagram #exam #onlineclasses #community #SoftwareDevelopment #Debugging #CleanCode #CodeReview #DevOps #Microservices #RESTAPI #Testing #ContinuousIntegration #UXDesign #UIUX #MobileDev #ProgressiveWebApps #TypeScriptTips #JavaScriptTips #CodingChallenges #LearnToCode #TechInspiration #CloudComputing #APIs #Automation #TechLearning #CareerGrowth #DigitalTransformation #Innovation #TechTrends #opentowork #governersindhinitiative

    Always Tag these people :
    M.Suhaib Umair, Ameen Alam, Daniyal Nagori, Asharib Ali, Hamza Alvi, Hamzah Syed, Fahad Khan, Syed Shah Meer Ali Taimoor Kamran, Zia Khan, Hira Khan

    You can add more relevant hashtags  if they help boost reach and engagement.

    Keep posts concise, professional, and tailored to engage the tech community and learners. Include trends or news when applicable.

    always in shortest way 
    """,

    model=model
)


# chainlit decorator for when a new chat session starts
@cl.on_chat_start
async def handle_chat_start():
    # Send welcome message to user
    await cl.Message(content="👋 Hi! I'm your Social Media Post Agent. Ready to help you plan and post engaging content about your tech journey—Python, JS/TS, Next.js, AI & more. Let's grow your presence with smart, hashtag-optimized posts!").send()

# chainlit decorator for when a new message is received
@cl.on_message
async def handle_message(message: cl.Message):
    # Get the message content from user
    prompt=message.content
    output=Runner.run_sync(starting_agent=agent, input=prompt)
    await cl.Message(output.final_output).send()
