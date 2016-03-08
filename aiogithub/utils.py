from functools import wraps


# from aiogithub.exceptions import FieldNotLoaded

def return_key(func):
    @wraps(func)
    def wrapper(self):
        try:
            return self[func.__name__]
        except KeyError:
            # raise FieldNotLoaded
            return None

    return wrapper
