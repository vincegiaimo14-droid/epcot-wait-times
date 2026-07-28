"""
Fetches current EPCOT wait times from Queue-Times.com and appends
one summary record to data/epcot_waits.json.

This script is designed to be run automatically every hour by a
GitHub Actions workflow (see .github/workflows/fetch.yml).

Data source: Queue-Times.com (https://queue-times.com)
Attribution required: "Powered by Queue-Times.com"
"""

import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen, Request

EPCOT_PARK_ID = 5
API_URL = f"https://queue-times.com/parks/{EPCOT_PARK_ID}/queue_times.json"
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "epcot_waits.json")


def fetch_current_wait_times():
    """Call the Queue-Times API and return the raw JSON."""
    req = Request(API_URL, headers={"User-Agent": "epcot-wait-tracker (learning project)"})
    with urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())


def summarize(raw_data):
    """
    Turn the raw lands/rides structure into one simple summary record:
    - timestamp
    - average wait time across all currently open rides
    - number of rides open
    - number of rides closed
    """
    all_waits = []
    open_count = 0
    closed_count = 0

    for land in raw_data.get("lands", []):
        for ride in land.get("rides", []):
            if ride.get("is_open"):
                open_count += 1
                all_waits.append(ride.get("wait_time", 0))
            else:
                closed_count += 1

    average_wait = round(sum(all_waits) / len(all_waits), 1) if all_waits else None

    now = datetime.now(timezone.utc)
    return {
        "timestamp_utc": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "hour_utc": now.hour,
        "day_of_week": now.strftime("%A"),
        "average_wait_minutes": average_wait,
        "rides_open": open_count,
        "rides_closed": closed_count,
    }


def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(records):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)


def main():
    raw = fetch_current_wait_times()
    record = summarize(raw)

    records = load_existing_data()
    records.append(record)

    save_data(records)
    print(f"Saved record: {record}")


if __name__ == "__main__":
    main()
