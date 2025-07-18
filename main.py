from gmail_auth import gmail_authenticate
from email_fetcher import get_latest_emails
from email_summariser import summarise_email
import json
import os


def main():
    service = gmail_authenticate()
    emails = get_latest_emails(service)

    os.makedirs("output", exist_ok=True)
    with open("output/raw_emails.json", "w") as f:
        json.dump(emails, f, indent=4)

    summaries = []
    for email in emails:
        summary = summarise_email(email["body"])
        summaries.append({"subject": email["subject"], "summary": summary})

    with open("output/summaries.json", "w") as f:
        json.dump(summaries, f, indent=4)

    print("✅ Summarization complete. Check output/summaries.json")


if __name__ == "__main__":
    main()
