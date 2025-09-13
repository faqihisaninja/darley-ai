from typing import List, Dict, Any
from datetime import datetime, timedelta
import pytz


def get_upcoming_events(service, days_ahead: int = 1) -> List[Dict[str, Any]]:
    # Set timezone to Australia/Sydney
    sydney_tz = pytz.timezone("Australia/Sydney")
    now = datetime.now(sydney_tz)

    # Start from current time in Sydney timezone
    time_min = now.isoformat()

    # End at 11:59:59 PM of the target day (now + days_ahead)
    target_date = now + timedelta(days=days_ahead)
    end_of_target_day = target_date.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    time_max = end_of_target_day.isoformat()
    events_result: Dict[str, Any] = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])
