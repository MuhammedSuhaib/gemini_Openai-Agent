import requests
import json
from agents import function_tool

@function_tool
def get_muhammad_suhaib_profile() -> str:
    """
    Retrieves the complete professional profile of Muhammad Suhaib.
    
    Use this tool to answer any questions regarding Suhaib's:
    - Bio and personal background (/about-me)
    - Technical skills and stack (/tech-stack)
    - Portfolio projects and case studies (/projects)
    - Career timeline and history
    
    The tool returns a comprehensive JSON object containing all these sections.
    """
    url = "https://muhammadsuhaibapi.netlify.app/"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Return as a formatted string so the agent can parse it easily
            return json.dumps(response.json(), indent=2)
        return f"Error: API unreachable (Status: {response.status_code})"
    except Exception as e:
        return f"Error connecting to profile API: {str(e)}"