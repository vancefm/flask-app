from flask import current_app
from functools import wraps
from utils.errors.custom_exception import CustomException


def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            current_app.logger.error("Custom Exception received")
        except Exception as e:
            current_app.logger.error("Generic Exception received")
    return error_wrapper
