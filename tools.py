# tools.py
from typing import Dict, Any
from email_utils.email_fetcher import get_latest_emails
from calendar_utils.google_calendar import get_upcoming_events
from email_utils.email_summariser import summarise_email


def get_emails_tool(service, max_results: int = 5) -> Dict[str, Any]:
    """Get latest emails from Gmail inbox"""
    try:
        emails = get_latest_emails(service, max_results)
        return {
            "success": True,
            "emails": emails,
            "count": len(emails),
            "message": f"Retrieved {len(emails)} emails from inbox",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to fetch emails: {str(e)}",
            "emails": [],
        }


def get_calendar_tool(service, days_ahead: int = 1) -> Dict[str, Any]:
    """Get upcoming calendar events"""
    try:
        events = get_upcoming_events(service, days_ahead)
        return {
            "success": True,
            "events": events,
            "count": len(events),
            "days_ahead": days_ahead,
            "message": f"Retrieved {len(events)} events for next {days_ahead} day(s)",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to fetch calendar events: {str(e)}",
            "events": [],
        }


def summarize_email_tool(email_body: str) -> Dict[str, Any]:
    """Summarize email content"""
    try:
        summary = summarise_email(email_body)
        return {
            "success": True,
            "summary": summary,
            "message": "Email summarized successfully",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to summarize email: {str(e)}",
            "summary": "Unable to summarize this email",
        }
