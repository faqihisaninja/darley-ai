# tool_definitions.py
from google.genai import types

# Define the tools for Gemini
EMAIL_TOOL = types.FunctionDeclaration(
    name="get_emails",
    description="Get latest emails from Gmail inbox",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "max_results": types.Schema(
                type="INTEGER",
                description="Maximum number of emails to retrieve (default: 5)",
            )
        },
    ),
)

CALENDAR_TOOL = types.FunctionDeclaration(
    name="get_calendar",
    description="Get upcoming calendar events",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "days_ahead": types.Schema(
                type="INTEGER",
                description="Number of days ahead to look for events (default: 7)",
            )
        },
    ),
)

SUMMARIZE_TOOL = types.FunctionDeclaration(
    name="summarize_email",
    description="Summarize email content",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "email_body": types.Schema(
                type="STRING", description="The email content to summarize"
            )
        },
        required=["email_body"],
    ),
)

# Bundle them together
ALL_TOOLS = [EMAIL_TOOL, CALENDAR_TOOL, SUMMARIZE_TOOL]
