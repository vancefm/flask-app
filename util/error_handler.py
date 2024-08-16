from flask import current_app
from functools import wraps


class CustomException(Exception):
    def __init__(self, message, errors):
        self.errors = errors
        super().__init__(message)

def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            current_app.logger.error("Custom Exception received")
            current_app.logger.error(f"Error List: {e.errors}")
    return error_wrapper
