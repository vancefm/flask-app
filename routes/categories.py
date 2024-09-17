from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from services import categories_service

categories_blueprint = Blueprint("categories_page", __name__, url_prefix="/categories")

@categories_blueprint.route("/")
@handle_errors
def categories_page():
    cg_list = categories_service.get_categories_with_parent_names()
    return render_template("categories_list.html", category_list=cg_list)
