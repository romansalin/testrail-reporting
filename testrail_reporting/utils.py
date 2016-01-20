from datetime import datetime

import pytz


def timestamp_to_utc_date(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=pytz.utc)
