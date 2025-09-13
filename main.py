from calendar_utils.google_calendar import GoogleCalendarProvider, get_upcoming_events
from email_utils.gmail_auth import gmail_authenticate
from email_utils.email_fetcher import get_latest_emails
from email_utils.email_summariser import summarise_email
import json
import os
from typing import List, Dict, Any
from googleapiclient.discovery import Resource
from provider_auth.google_auth import GoogleAuthManager


def main() -> None:
    # calendar = GoogleCalendarProvider()
    # calendar.authenticate()
    # events = calendar.get_upcoming_events(48)
    # for e in events:
    #     print(e["summary"], e["start"].get("dateTime"))

    # service: Resource = gmail_authenticate()
    # emails: List[Dict[str, str]] = get_latest_emails(service)

    # os.makedirs("output", exist_ok=True)
    # with open("output/raw_emails.json", "w") as f:
    #     json.dump(emails, f, indent=4)

    # summaries: List[Dict[str, str]] = []
    # for email in emails:
    #     summary: str = summarise_email(email["body"])
    #     summaries.append({"subject": email["subject"], "summary": summary})

    # with open("output/summaries.json", "w") as f:
    #     json.dump(summaries, f, indent=4)

    # print("✅ Summarization complete. Check output/summaries.json")
    custom_scopes = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/calendar.readonly",
    ]

    auth_manager = GoogleAuthManager(
        scopes=custom_scopes,
        token_path="token.json",
        creds_path="credentials.json",
    )
    gmail_service = auth_manager.authenticate("gmail", "v1")
    calendar_service = auth_manager.authenticate("calendar", "v3")
    events = get_upcoming_events(calendar_service)
    for e in events:
        print(e["summary"], e["start"].get("dateTime"))


if __name__ == "__main__":
    main()
