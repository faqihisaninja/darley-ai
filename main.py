from calendar_utils.google_calendar import GoogleCalendarProvider
from email_utils.gmail_auth import gmail_authenticate
from email_utils.email_fetcher import get_latest_emails
from email_utils.email_summariser import summarise_email
import json
import os
from typing import List, Dict, Any
from googleapiclient.discovery import Resource


def main() -> None:
    calendar = GoogleCalendarProvider()
    calendar.authenticate()
    events = calendar.get_upcoming_events(48)
    for e in events:
        print(e["summary"], e["start"].get("dateTime"))

    service: Resource = gmail_authenticate()
    emails: List[Dict[str, str]] = get_latest_emails(service)

    os.makedirs("output", exist_ok=True)
    with open("output/raw_emails.json", "w") as f:
        json.dump(emails, f, indent=4)

    summaries: List[Dict[str, str]] = []
    for email in emails:
        summary: str = summarise_email(email["body"])
        summaries.append({"subject": email["subject"], "summary": summary})

    with open("output/summaries.json", "w") as f:
        json.dump(summaries, f, indent=4)

    print("✅ Summarization complete. Check output/summaries.json")


if __name__ == "__main__":
    main()
