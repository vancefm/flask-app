from flask import current_app, render_template
from functools import wraps
from utils.errors.custom_exception import CustomException
import traceback

def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            current_app.logger.error(f"Custom Exception: {e}\n{traceback.format_exc()}")
            return render_template("error.html"), 500
        except Exception as e:
            current_app.logger.error(f"Generic Exception: {e}\n{traceback.format_exc()}")
            return render_template("error.html"), 500
    return error_wrapper