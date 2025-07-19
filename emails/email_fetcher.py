import base64
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import Resource


def get_latest_emails(service: Resource, max_results: int = 5) -> List[Dict[str, str]]:
    result: Dict[str, Any] = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=max_results)
        .execute()
    )
    messages: List[Dict[str, str]] = result.get("messages", [])
    emails: List[Dict[str, str]] = []

    for msg in messages:
        try:
            txt: Dict[str, Any] = (
                service.users().messages().get(userId="me", id=msg["id"]).execute()
            )
            payload: Dict[str, Any] = txt["payload"]
            headers: List[Dict[str, str]] = payload["headers"]
            subject: str = next(h["value"] for h in headers if h["name"] == "Subject")
            parts: List[Dict[str, Any]] = payload.get("parts", [])
            data: str = ""

            for part in parts:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    data = part["body"]["data"]
                    break
            if not data and "data" in payload.get("body", {}):
                data = payload["body"]["data"]

            decoded_body: str = base64.urlsafe_b64decode(data).decode("utf-8")
            emails.append({"subject": subject, "body": decoded_body})

        except Exception as e:
            print("Error reading message:", e)

    return emails
