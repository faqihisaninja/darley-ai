# email_summariser.py
from google import genai
from google.genai import types
from config import GOOGLE_STUDIO_API_KEY

# Initialize the client
client = genai.Client(api_key=GOOGLE_STUDIO_API_KEY)


def summarise_email(email_body: str) -> str:
    """Summarize email content using Gemma 2 27B model"""

    prompt = f"""
        Please provide a concise summary of the following email content:

        Email Content:
        {email_body}

        Summary Guidelines:
        - Keep it brief but comprehensive
        - Highlight key points and action items
        - Identify the main purpose/request
        - Note any deadlines or urgent matters
        - Use bullet points for clarity

        Summary:
        """

    try:
        response = client.models.generate_content(
            model="models/gemma-3-27b-it",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=300,
                top_p=0.95,
            ),
        )
        return response.text

    except Exception as e:
        return f"Error summarizing email: {str(e)}"
