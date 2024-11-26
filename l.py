import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("AFRICASTALKING_USERNAME")
api_key = os.getenv("AFRICASTALKING_API_KEY")

print(f"Username: {username}, API Key: {api_key}")