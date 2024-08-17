from flask import current_app, Blueprint, render_template
from functools import wraps
from utils.errors.custom_exception import CustomException

error_blueprint = Blueprint("error_page", __name__, template_folder="../../templates")

def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            current_app.logger.error("Custom Exception received")
            return error_page()
        except Exception as e:
            current_app.logger.error("Generic Exception received")
    return error_wrapper

@error_blueprint.errorhandler(CustomException)
def error_page():
    return render_template("error.html"), 500

@error_blueprint.errorhandler(Exception)
def error_page():
    return render_template("error.html"), 500