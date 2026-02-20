"""Contest calendar date resolution engine.

Pure Python — no ClickHouse dependency. Resolves contest dates from
scheduling rules (YAML) and builds upcoming/full-year schedules.
"""

from __future__ import annotations

import calendar
import datetime as dt
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------------------
# Weekend math
# ---------------------------------------------------------------------------

def _full_weekends_in_month(year: int, month: int) -> list[dt.date]:
    """Return Saturday dates where both Sat and Sun fall within the month.

    A "full weekend" means Saturday AND Sunday are both in the named month.
    """
    _, last_day = calendar.monthrange(year, month)
    saturdays = []
    for day in range(1, last_day + 1):
        d = dt.date(year, month, day)
        if d.weekday() == 5:  # Saturday
            sunday = d + dt.timedelta(days=1)
            if sunday.month == month:
                saturdays.append(d)
    return saturdays


def resolve_contest_date(rule: dict, year: int) -> dt.datetime | None:
    """Resolve a contest rule to a start datetime for the given year.

    Returns UTC datetime of the contest start, or None if the rule
    can't be resolved (e.g., not enough weekends).
    """
    month = rule["month"]
    weekends = _full_weekends_in_month(year, month)
    if not weekends:
        return None

    weekend_rule = rule["weekend_rule"]
    if weekend_rule == "last_full_weekend":
        saturday = weekends[-1]
    elif weekend_rule == "first_full_weekend":
        saturday = weekends[0]
    elif weekend_rule == "nth_full_weekend":
        n = rule.get("n", 1)
        if n > len(weekends):
            return None
        saturday = weekends[n - 1]
    else:
        return None

    # Adjust for Friday starts (move back 1 day)
    start_day = rule.get("start_day", "saturday")
    if start_day == "friday":
        start_date = saturday - dt.timedelta(days=1)
    else:
        start_date = saturday

    # Parse start time
    start_utc = rule.get("start_utc", "00:00")
    hour, minute = (int(x) for x in start_utc.split(":"))

    return dt.datetime(start_date.year, start_date.month, start_date.day,
                       hour, minute)


# ---------------------------------------------------------------------------
# Schedule builders
# ---------------------------------------------------------------------------

def build_contest_schedule(
    contests: list[dict],
    now: dt.datetime,
    horizon_days: int = 365,
) -> list[dict]:
    """Resolve all contests for current + next year, add computed fields.

    Each entry gets: start, end, days_until, status.
    Returns sorted by start date, filtered to horizon window.
    """
    cutoff = now + dt.timedelta(days=horizon_days)
    current_year = now.year
    scheduled = []

    for contest in contests:
        rule = contest["rule"]
        duration = dt.timedelta(hours=rule.get("duration_hours", 48))

        for year in (current_year, current_year + 1):
            start = resolve_contest_date(rule, year)
            if start is None:
                continue
            end = start + duration

            # Skip if entirely in the past or beyond horizon
            if end < now:
                continue
            if start > cutoff:
                continue

            days_until = (start - now).total_seconds() / 86400

            if now >= start and now <= end:
                status = "active"
            elif days_until <= 0:
                status = "past"
            else:
                status = "upcoming"

            scheduled.append({
                "name": contest["name"],
                "sponsor": contest.get("sponsor", ""),
                "modes": contest.get("modes", []),
                "bands": contest.get("bands", []),
                "url": contest.get("url", ""),
                "description": contest.get("description", ""),
                "start": start,
                "end": end,
                "duration_hours": rule.get("duration_hours", 48),
                "days_until": days_until,
                "status": status,
            })

    scheduled.sort(key=lambda x: x["start"])
    return scheduled


def upcoming_contests(scheduled: list[dict], days: int = 30) -> list[dict]:
    """Filter schedule to contests starting within N days (or active now)."""
    return [
        c for c in scheduled
        if c["status"] == "active" or (c["status"] == "upcoming" and c["days_until"] <= days)
    ]


def build_dxpedition_schedule(
    dxpeditions: list[dict],
    now: dt.datetime,
) -> list[dict]:
    """Filter and annotate DXpeditions: active + upcoming only."""
    today = now.date()
    results = []

    for dx in dxpeditions:
        start = dt.date.fromisoformat(dx["start_date"])
        end = dt.date.fromisoformat(dx["end_date"])

        # Skip past DXpeditions
        if end < today:
            continue

        days_until = (start - today).days

        if today >= start and today <= end:
            status = "active"
            days_until = 0
        elif days_until > 0:
            status = "upcoming"
        else:
            continue

        results.append({
            **dx,
            "start": start,
            "end": end,
            "days_until": days_until,
            "status": status,
        })

    results.sort(key=lambda x: x["start"])
    return results


# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------

def load_contests(path: Path | None = None) -> list[dict]:
    """Load contest rules from YAML."""
    p = path or (DATA_DIR / "contests.yaml")
    with open(p) as f:
        return yaml.safe_load(f)


def load_dxpeditions(path: Path | None = None) -> dict:
    """Load DXpedition data from YAML. Returns full dict with calendars + dxpeditions."""
    p = path or (DATA_DIR / "dxpeditions.yaml")
    with open(p) as f:
        return yaml.safe_load(f)
