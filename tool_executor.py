# tool_executor.py
from typing import Dict, Any
from tools import get_emails_tool, get_calendar_tool, summarize_email_tool


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

        else:
            return {"success": False, "error": f"Unknown function: {function_name}"}
