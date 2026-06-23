from datetime import datetime
from typing import TypedDict

import pytz
from fastapi import FastAPI

app = FastAPI(title="Time API - Colombia, EEUU, France", version="1.0.0")


class TimeData(TypedDict):
    """Type for time data response."""

    timezone: str
    time: str
    hour: int
    minute: int


class TimeResponse(TypedDict):
    """Response structure for time endpoint."""

    colombia: TimeData
    eeuu: TimeData
    france: TimeData


@app.get("/time", response_model=TimeResponse)
def get_time() -> TimeResponse:
    """Return the current time in Colombia, EEUU, and France."""
    timezones = {
        "colombia": "America/Bogota",
        "eeuu": "America/New_York",
        "france": "Europe/Paris",
    }

    result: TimeResponse = {}

    for country, tz_name in timezones.items():
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        result[country] = {
            "timezone": tz_name,
            "time": now.isoformat(),
            "hour": now.hour,
            "minute": now.minute,
        }

    return result


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
