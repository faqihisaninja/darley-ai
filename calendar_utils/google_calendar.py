from typing import List, Dict, Any, Optional
from googleapiclient.discovery import Resource
from datetime import datetime, timedelta

from provider_auth import create_calendar_auth_manager


class GoogleCalendarProvider:
    def __init__(
        self, token_path: str = "token.json", creds_path: str = "credentials.json"
    ) -> None:
        self.auth_manager = create_calendar_auth_manager(token_path, creds_path)
        self.service: Optional[Resource] = None

    def authenticate(self) -> None:
        self.service = self.auth_manager.authenticate("calendar", "v3")

    def get_upcoming_events(self, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        now: str = datetime.now().isoformat() + "Z"
        later: str = (datetime.now() + timedelta(hours=hours_ahead)).isoformat() + "Z"
        events_result: Dict[str, Any] = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                timeMax=later,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])
