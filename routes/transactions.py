from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from utils.data_import import DataImporter

transactions_blueprint = Blueprint("transactions_page", __name__, url_prefix="/transactions")

@transactions_blueprint.route("/")
@handle_errors
def transactions_page():
    with current_app.app_context():
        importer = DataImporter()
        tx_list = importer.transaction_list
        cg_list = importer.category_list
    return render_template("transaction_list.html", transaction_list=tx_list, category_list=cg_list)

@transactions_blueprint.route("/update-transaction/<int:transaction_id>", methods=['POST'])
@handle_errors
def update_transaction(transaction):
    current_app.logger.info("Transaction updated.")