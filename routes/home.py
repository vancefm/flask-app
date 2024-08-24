from flask import current_app, Blueprint, render_template
from utils.errors.error_handler import handle_errors

home_blueprint = Blueprint("home_blueprint", __name__, template_folder="../templates")

@home_blueprint.route("/home")
@handle_errors
def root_route():
    current_app.logger.info("Home route accessed.")
    return render_template("test.html"), 200


