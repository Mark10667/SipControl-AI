from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from parent directory
dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

# Print environment variables (with partial masking for security)
def mask_string(s):
    if s:
        return s[:4] + '*' * (len(s) - 4)
    return None

print("Environment Variables:")
print(f"AZURE_API_KEY: {mask_string(os.getenv('AZURE_API_KEY'))}")
print(f"AZURE_ENDPOINT: {os.getenv('AZURE_ENDPOINT')}")
print(f"GPT4_DEPLOYMENT: {os.getenv('GPT4_DEPLOYMENT')}") 