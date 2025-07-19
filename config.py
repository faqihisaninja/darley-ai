import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

GOOGLE_STUDIO_API_KEY: str = os.getenv("GOOGLE_STUDIO_API_KEY", "")
# If modifying these scopes, delete the file token.json.
SCOPES: List[str] = ["https://www.googleapis.com/auth/gmail.readonly"]
