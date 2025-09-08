import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_STUDIO_API_KEY: str = os.getenv("GOOGLE_STUDIO_API_KEY", "")
