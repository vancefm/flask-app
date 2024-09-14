from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from data.models.category import Category

categories_blueprint = Blueprint("categories_page", __name__, url_prefix="/categories")

@categories_blueprint.route("/")
@handle_errors
def categories_page():
    cg_list = Category.query.all()
    return render_template("categories_list.html", category_list=cg_list)
