from datetime import datetime
from typing import TypedDict

import pytz
from fastapi import FastAPI

app = FastAPI(title="Day of Week API - Colombia, China, España", version="1.0.0")


class DayData(TypedDict):
    """Type for day of week data response."""

    timezone: str
    day_of_week: str
    day_number: int
    date: str


class DayResponse(TypedDict):
    """Response structure for day endpoint."""

    colombia: DayData
    china: DayData
    espana: DayData


@app.get("/day", response_model=DayResponse)
def get_day() -> DayResponse:
    """Return the current day of week in Colombia, China, and España."""
    timezones = {
        "colombia": "America/Bogota",
        "china": "Asia/Shanghai",
        "espana": "Europe/Madrid",
    }

    result: DayResponse = {}

    for country, tz_name in timezones.items():
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        result[country] = {
            "timezone": tz_name,
            "day_of_week": ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")[now.weekday()],
            "day_number": now.weekday(),
            "date": now.strftime("%Y-%m-%d"),
        }

    return result


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
