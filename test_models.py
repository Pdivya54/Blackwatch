import anthropic
import os
from dotenv import load_dotenv
from core.config import settings
from anthropic import Anthropic
# Load the .env file
load_dotenv()

# Print a partial key to verify it loaded
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"API Key loaded: {api_key[:15]}...") # Prints first 8 characters
else:
    print("Error: ANTHROPIC_API_KEY not found in environment!")

# Use the Pydantic-validated settings object
client = Anthropic(api_key=settings.anthropic_api_key)

# Now test it
print(f"Testing with key: {settings.anthropic_api_key[:8]}...")
# ... proceed with test

import anthropic
client = anthropic.Anthropic(api_key="sk-ant-api03-...") # Paste your ACTUAL key here
print(client.models.list())