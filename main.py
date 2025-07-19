from emails.gmail_auth import gmail_authenticate
from emails.email_fetcher import get_latest_emails
from emails.email_summariser import summarise_email
import json
import os
from typing import List, Dict, Any
from googleapiclient.discovery import Resource


def main() -> None:
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
