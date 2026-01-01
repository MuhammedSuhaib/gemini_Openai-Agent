import os
from chainlit.cli import run_chainlit
from main import *

if __name__ == "__main__":
    # Set default port for Hugging Face Spaces if not provided
    if not os.environ.get("PORT"):
        os.environ["PORT"] = "7860"
    
    # Run the Chainlit app
    run_chainlit("main.py")