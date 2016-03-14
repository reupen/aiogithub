from functools import wraps


# from aiogithub.exceptions import FieldNotLoaded

def return_key(func):
    @wraps(func)
    def wrapper(self):
        return self.get(func.__name__)

    return wrapper
