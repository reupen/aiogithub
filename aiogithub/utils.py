from functools import wraps


def return_key(func):
    @wraps(func)
    def wrapper(self):
        return self[func.__name__]

    return wrapper
