from datetime import datetime

import pytz


def get_now():
    return datetime.now(tz=pytz.utc)


def timestamp_to_dt(timestamp):
    try:
        return datetime.fromtimestamp(float(timestamp), tz=pytz.utc)
    except (ValueError, TypeError):
        return None


def get_dt_iso(dt=datetime.now(), sep='T'):
    if not isinstance(dt, datetime):
        return None
    return dt.replace(microsecond=0).isoformat(sep)


def chunks(lst, n):
    """Split a list into evenly sized chunks."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]


class LazyWrapper(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        try:
            return self.value
        except AttributeError:
            self.value = self.func()
            return self.value
