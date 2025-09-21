# tools.py
from typing import Dict, Any
from email_utils.email_fetcher import get_latest_emails
from calendar_utils.google_calendar import get_upcoming_events
from email_utils.email_summariser import summarise_email


# Emails
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


# Calendar
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


def create_calendar_event_tool(
    service,
    title: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
) -> Dict[str, Any]:
    """Create a new calendar event"""
    try:
        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Australia/Sydney",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Australia/Sydney",
            },
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        return {
            "success": True,
            "event_id": created_event["id"],
            "event_link": created_event.get("htmlLink", ""),
            "message": f"Created event '{title}' from {start_time} to {end_time}",
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to create event: {str(e)}"}


def edit_calendar_event_tool(
    service,
    event_id: str,
    title: str = None,
    start_time: str = None,
    end_time: str = None,
    description: str = None,
    location: str = None,
) -> Dict[str, Any]:
    """Edit an existing calendar event"""
    try:
        # Get the existing event first
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        # Update only the provided fields
        if title:
            event["summary"] = title
        if start_time:
            event["start"] = {"dateTime": start_time, "timeZone": "Australia/Sydney"}
        if end_time:
            event["end"] = {"dateTime": end_time, "timeZone": "Australia/Sydney"}
        if description is not None:
            event["description"] = description
        if location is not None:
            event["location"] = location

        updated_event = (
            service.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )

        return {
            "success": True,
            "event_id": updated_event["id"],
            "message": f"Updated event '{updated_event.get('summary', 'Unknown')}'",
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to edit event: {str(e)}"}
