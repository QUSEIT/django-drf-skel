import traceback
from functools import wraps

from portal.settings import DEBUG
from portal.celery_tasks import notify_exception_message


def catch_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DEBUG:
            return func(*args, **kwargs)
        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            log = traceback.format_exc()
            notify_exception_message.delay(log)
    return wrapper
