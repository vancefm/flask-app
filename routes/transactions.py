from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from data.models import db
from data.models.transaction import Transaction
from sqlalchemy import select
from services import categories_service

transactions_blueprint = Blueprint("transactions_page", __name__, url_prefix="/transactions")

@transactions_blueprint.route("/")
@handle_errors
def transactions_page():
    with current_app.app_context():
        tx_list = db.session.execute(select(Transaction)).scalars().all()
        cg_list = categories_service.get_categories_with_parent_names()
        print(tx_list)
        print("")
        print(cg_list)
        tx_dict = {tx.id: tx for tx in tx_list}
    return render_template("transaction_list.html", transaction_dict=tx_dict, category_list=cg_list)

@transactions_blueprint.route("/update-transaction/<int:transaction_id>", methods=['POST'])
@handle_errors
def update_transaction(transaction):
    current_app.logger.info("Transaction updated.")