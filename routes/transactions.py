from flask import current_app, render_template, Blueprint
from utils.errors.error_handler import handle_errors
from data.models import db
from data.models.category import Category
from data.models.transaction import Transaction
from sqlalchemy import select

transactions_blueprint = Blueprint("transactions_page", __name__, url_prefix="/transactions")

@transactions_blueprint.route("/")
@handle_errors
def transactions_page():
    with current_app.app_context():
        tx_list = db.session.execute(select(Transaction)).scalars().all()
        cg_list = db.session.execute(select(Category)).scalars().all()
        
        tx_dict = {tx.id: tx for tx in tx_list}
        cg_dict = {cg.id: cg for cg in cg_list}
    return render_template("transaction_list.html", transaction_dict=tx_dict, category_dict=cg_dict)

@transactions_blueprint.route("/update-transaction/<int:transaction_id>", methods=['POST'])
@handle_errors
def update_transaction(transaction):
    current_app.logger.info("Transaction updated.")