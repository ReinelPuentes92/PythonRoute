from datetime import datetime, timezone

from fastapi import FastAPI

app = (title="Hour API POC")


@app.get("/hour")
def get_hour() -> dict[str, int | str]:
    """Return the current UTC time with hour-focused fields."""
    now = datetime.now(timezone.utc)
    return {
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "iso_utc": now.isoformat(),
    }
