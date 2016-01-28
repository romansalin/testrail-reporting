from datetime import datetime

import pytz


def get_now():
    return datetime.now(tz=pytz.utc)


def timestamp_to_utc(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=pytz.utc)


def get_dt_iso(dt=datetime.now(), sep='T'):
    if not isinstance(dt, datetime):
        return None
    return dt.replace(microsecond=0).isoformat(sep)


def chunks(lst, n):
    """Split a list into evenly sized chunks."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]
