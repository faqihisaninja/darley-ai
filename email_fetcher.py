import base64


def get_latest_emails(service, max_results=5):
    result = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=max_results)
        .execute()
    )
    messages = result.get("messages", [])
    emails = []

    for msg in messages:
        try:
            txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = txt["payload"]
            headers = payload["headers"]
            subject = next(h["value"] for h in headers if h["name"] == "Subject")
            parts = payload.get("parts", [])
            data = ""

            for part in parts:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    data = part["body"]["data"]
                    break
            if not data and "data" in payload.get("body", {}):
                data = payload["body"]["data"]

            decoded_body = base64.urlsafe_b64decode(data).decode("utf-8")
            emails.append({"subject": subject, "body": decoded_body})

        except Exception as e:
            print("Error reading message:", e)

    return emails
