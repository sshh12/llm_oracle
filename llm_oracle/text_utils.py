import datetime

TIME_UNITS = {"year": 365, "month": 31, "week": 7, "day": 1}


def future_date_to_string(raw_date: datetime.datetime) -> str:
    date = raw_date.replace(tzinfo=None)
    s = date.isoformat()[:10]
    days_from_now = (date - datetime.datetime.now()).days
    rel = None
    for unit, unit_days in TIME_UNITS.items():
        if days_from_now > unit_days:
            rel = f"~ {days_from_now/unit_days:.1f} {unit}s"
            break
    return f"{s} (in {rel})"


def world_state_to_string() -> str:
    state = {"current_date": datetime.datetime.now().isoformat()[:10]}
    return "\n".join([f"{k}: {v}" for k, v in state.items()])
