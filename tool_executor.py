# tool_executor.py
from typing import Dict, Any
from tools import (
    get_emails_tool,
    summarize_email_tool,
    get_calendar_tool,
    create_calendar_event_tool,
    edit_calendar_event_tool,
)


class ToolExecutor:
    """Executes tool functions based on Gemini function calls"""

    def __init__(self, gmail_service, calendar_service):
        self.gmail_service = gmail_service
        self.calendar_service = calendar_service

    def execute_tool(
        self, function_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool based on the function name and arguments"""

        if function_name == "get_emails":
            max_results = arguments.get("max_results", 5)
            return get_emails_tool(self.gmail_service, max_results)

        elif function_name == "get_calendar":
            days_ahead = arguments.get("days_ahead", 1)
            return get_calendar_tool(self.calendar_service, days_ahead)

        elif function_name == "summarize_email":
            email_body = arguments.get("email_body", "")
            if not email_body:
                return {"success": False, "error": "No email body provided"}
            return summarize_email_tool(email_body)
        elif function_name == "create_calendar_event":
            title = arguments.get("title", "")
            start_time = arguments.get("start_time", "")
            end_time = arguments.get("end_time", "")
            description = arguments.get("description", "")
            location = arguments.get("location", "")
            return create_calendar_event_tool(
                self.calendar_service,
                title,
                start_time,
                end_time,
                description,
                location,
            )

        elif function_name == "edit_calendar_event":
            event_id = arguments.get("event_id", "")
            title = arguments.get("title")
            start_time = arguments.get("start_time")
            end_time = arguments.get("end_time")
            description = arguments.get("description")
            location = arguments.get("location")
            return edit_calendar_event_tool(
                self.calendar_service,
                event_id,
                title,
                start_time,
                end_time,
                description,
                location,
            )

        else:
            return {"success": False, "error": f"Unknown function: {function_name}"}
