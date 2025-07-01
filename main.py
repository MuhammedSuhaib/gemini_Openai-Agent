import chainlit as cl
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
#                                   ⬆               ⬆
#                                 Just bcz i m using gemini
from agents.run import RunConfig
from dotenv import load_dotenv
load_dotenv()
from typing import Optional, Dict, cast  # Type hints for better code clarity
from colorama import Fore, init

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# Check if the API key is present; if not, raise an error
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Decorator to handle OAuth callback from GitHub
@cl.oauth_callback
def oauth_callback(
    provider_id: str,  # ID of the OAuth provider (GitHub)
    token: str,  # OAuth access token
    raw_user_data: Dict[str, str],  # User data from GitHub
    default_user: cl.User,  # Default user object from Chainlit
) -> Optional[cl.User]:  # Return User object or None
    """
    Handle the OAuth callback from GitHub
    Return the user object if authentication is successful, None otherwise
    """

    print(f"Provider: {provider_id}")  # Print provider ID for debugging
    print(f"User data: {raw_user_data}")  # Print user data for debugging

    return default_user  # Return the default user object

@cl.on_chat_start
async def start():

    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
    )

    model = OpenAIChatCompletionsModel(
        model='gemini-2.0-flash',
        openai_client=external_client 
    )

    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])

    agent = Agent(
        name='SocialMediaPoster',
        instructions = 
        """
        Only generate a LinkedIn and Twitter post *when clearly asked*. Do nothing if the message doesn't request a post (e.g., "hi", "how are you", etc.).

        When asked, create short, engaging, and clear content focused on my learning in tech (Python, JS/TS, Next.js, AI, etc.). Always add these hashtags:

        #LearningJourney #Python #WebDevelopment #JavaScript #TypeScript #js #ts #NextJS #NodeJS #Jamstack #Frontend #Backend #FullStack #DeveloperLife #CodingHumor #AI #AIagents #Programming #TechCommunity #1000Followers #CodingLife #piaic #giaic #React #TailwindCSS #CSS #HTML #DevCommunity #SoftwareEngineering #TechTips #OpenSource #CodeNewbie #100DaysOfCode #30DaysOf30Projects #genai #web3 #metaverse #students #studentlife #collegelife #education #studyabroad #learning #studentsuccess #hackathon #career #teachersofinstagram #exam #onlineclasses #community #SoftwareDevelopment #Debugging #CleanCode #CodeReview #DevOps #Microservices #RESTAPI #Testing #ContinuousIntegration #UXDesign #UIUX #MobileDev #ProgressiveWebApps #TypeScriptTips #JavaScriptTips #CodingChallenges #LearnToCode #TechInspiration #CloudComputing #APIs #Automation #TechLearning #CareerGrowth #DigitalTransformation #Innovation #TechTrends #opentowork #governersindhinitiative

        Always tag:
        @M.Suhaib Umair, @Ameen Alam, @Daniyal Nagori, @Asharib Ali, @Hamza Alvi, @Hamzah Syed, @Fahad Khan, @Bilal Muhammad Khan, @Bilal Fareed, @Syed Shah Meer Ali, @Naeem Hussain, @Taimoor Kamran, @Zia Khan, @Hira Khan

        You can add more relevant hashtags if needed for better reach.

        Keep posts short, professional, and engaging. Use trends/news if relevant. Only post *when asked explicitly*.
        If the message is not a clear request for a post , do not respond. Avoid irrelevant or off-topic replies.
        """,
        model=model
    )

    cl.user_session.set("agent", agent)  # Store the agent in user session
    cl.user_session.set("config", RunConfig())  # Store default config in user session

    # Send welcome message to user
    await cl.Message(content="👋 Hi!  I'm your Social Media Post Agent. Ready to help you plan and post engaging content about your tech journey—Python, JS/TS, Next.js, AI & more. Let's grow your presence with smart, hashtag-optimized posts!").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print( "\n \t \t \t  CALLING_AGENT_WITH_CONTEXT\n", Fore.YELLOW + str(history) + "\n" + Fore.RESET )
        result = Runner.run_sync(starting_agent = agent,
                    input=history,
                    run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        
        # Optional: Log the interaction
        print(Fore.CYAN + f"User: {message.content} " + Fore.RESET)
        print(Fore.LIGHTGREEN_EX + f"Assistant: {response_content}" + Fore.RESET)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")