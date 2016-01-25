from datetime import datetime

import pytz


def timestamp_to_utc(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=pytz.utc)


def get_now_iso():
    return datetime.now().isoformat()
