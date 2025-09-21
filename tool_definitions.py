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


CREATE_EVENT_TOOL = types.FunctionDeclaration(
    name="create_calendar_event",
    description="Create a new calendar event",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "title": types.Schema(type="STRING", description="Event title/summary"),
            "start_time": types.Schema(
                type="STRING",
                description="Start time in ISO format (YYYY-MM-DDTHH:MM:SS)",
            ),
            "end_time": types.Schema(
                type="STRING",
                description="End time in ISO format (YYYY-MM-DDTHH:MM:SS)",
            ),
            "description": types.Schema(
                type="STRING", description="Event description (optional)"
            ),
            "location": types.Schema(
                type="STRING", description="Event location (optional)"
            ),
        },
        required=["title", "start_time", "end_time"],
    ),
)

EDIT_EVENT_TOOL = types.FunctionDeclaration(
    name="edit_calendar_event",
    description="Edit an existing calendar event",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "event_id": types.Schema(
                type="STRING", description="The ID of the event to edit"
            ),
            "title": types.Schema(
                type="STRING", description="New event title (optional)"
            ),
            "start_time": types.Schema(
                type="STRING", description="New start time in ISO format (optional)"
            ),
            "end_time": types.Schema(
                type="STRING", description="New end time in ISO format (optional)"
            ),
            "description": types.Schema(
                type="STRING", description="New event description (optional)"
            ),
            "location": types.Schema(
                type="STRING", description="New event location (optional)"
            ),
        },
        required=["event_id"],
    ),
)

# Bundle them together
ALL_TOOLS = [
    EMAIL_TOOL,
    CALENDAR_TOOL,
    SUMMARIZE_TOOL,
    CREATE_EVENT_TOOL,
    EDIT_EVENT_TOOL,
]
