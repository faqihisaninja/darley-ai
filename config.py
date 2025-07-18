import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_STUDIO_API_KEY = os.getenv("GOOGLE_STUDIO_API_KEY")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
