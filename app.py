from flask import Flask, current_app, request, render_template
from utils.errors.error_handler import handle_errors
from utils.config_loader import ConfigLoader
from services.data_import import DataImporter


app = Flask(__name__)

ConfigLoader.create_app(app)

@app.before_request
def request_logger():
    """ Log each request as it comes in
    """
    current_app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route("/")
@handle_errors
def root_route():
    return render_template("test.html")

@app.route("/transactions")
@handle_errors
def transactions_page():
    with app.app_context():
        importer = DataImporter()
        transaction_list = importer.import_csv()
    return render_template("transaction_list.html", transactions_list=transaction_list)

if __name__ == '__main__':
    app.run()