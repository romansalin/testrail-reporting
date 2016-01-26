from datetime import datetime

import pytz


def timestamp_to_utc(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=pytz.utc)


def get_now_iso(sep='T'):
    return datetime.now().replace(microsecond=0).isoformat(sep)


def chunks(lst, n):
    """Split a list into evenly sized chunks."""
    return [lst[i:i+n] for i in range(0, len(lst), n)]
