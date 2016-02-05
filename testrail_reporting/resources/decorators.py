from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO(rsalin)

        return f(*args, **kwargs)
    return decorated
