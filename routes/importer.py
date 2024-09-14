from flask import current_app, render_template, Blueprint, request, redirect
from utils.errors.error_handler import handle_errors
from data.models import db
from data.models.transaction import Transaction
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime

importer_blueprint = Blueprint("import_page", __name__, url_prefix="/import")

@importer_blueprint.route("/", methods=['GET', 'POST'])
@handle_errors
def import_page():
    if request.method == 'POST':
        current_app.logger.debug("Starting data import")
        if 'file' not in request.files:
            return redirect(request.url)
        current_app.logger.debug("Form field name 'file' detected in request")
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        current_app.logger.debug("File name detected for file")

        if file and file.filename.lower().endswith('csv'):
            filename = secure_filename(file.filename)
            current_app.logger.info(f"Importing file {filename}")
            file_path = os.path.join(current_app.config['DATA']['TX_IMPORT_PATH'], filename)
            current_app.logger.debug(f"Saving file to {file_path}")
            file.save(file_path)
            current_app.logger.debug("File saved")

            transactions = []
            with open(file_path, newline='') as csv_file:
                current_app.logger.debug(f"Reading {file_path}")
                csv_reader = csv.DictReader(csv_file)
                headers = csv_reader.fieldnames

                if not verify_csv_headers(headers):
                    current_app.logger.info(f"Failed to import {file_path}. Malformed CSV headers")
                    return f"Error: Malformed CSV headers: {headers}", 400
                current_app.logger.debug("File headers look okay")

                current_app.logger.debug("Processing transactions..")
                for row in csv_reader:
                    # Get the integer Posting Date value. Assumes format MM/DD/YYYY
                    int_posting_date = int(datetime.strptime(row['Posting Date'], '%m/%d/%Y').timestamp())

                    tx = Transaction(
                        posting_date = int_posting_date, 
                        description = row['Description'], 
                        amount = row['Amount'],
                        type = row['Type'],
                        end_balance = row['Balance'],
                        is_new = True,
                        category_id = 1
                    )
                    current_app.logger.debug(tx)
                    transactions.append(tx)
                db.session.bulk_save_objects(transactions)
                db.session.commit()
                current_app.logger.info(f"Imported {len(transactions)} transactions")
                return redirect('/transactions')

    return render_template('import.html')

def verify_csv_headers(header_row):
    csv_headers = current_app.config['DATA']['CSV_HEADERS']
    return all(header in header_row for header in csv_headers)