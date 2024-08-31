from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from utils.data_import import DataImporter

transactions_blueprint = Blueprint("transactions_page", __name__)

@transactions_blueprint.route("/transactions")
@handle_errors
def transactions_page():
    with current_app.app_context():
        importer = DataImporter()
        tx_list = importer.transaction_list
        cg_list = importer.category_list
    return render_template("transaction_list.html", transaction_list=tx_list, category_list=cg_list)