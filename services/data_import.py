from flask import current_app
import pandas
from models.transaction import Transaction

class DataImporter:

    def __init__(self):
        self.csv_data_path = f"{current_app.config['DATA']['DATA_IMPORT_PATH']}"

    def import_csv(self):
        """Imports a CSV file

        Returns:
            _type_: _description_
        """
        try:
            csv_dataframe = pandas.read_csv(self.csv_data_path, index_col=False)
            #print(csv_dataframe)
            transaction_list = csv_dataframe.apply(
                lambda row: 
                Transaction(
                    row['Posting Date'], 
                    row['Description'], 
                    row['Amount'],
                    row['Type'],
                    row['Balance'],
                    is_new=True), axis=1).tolist()
            return transaction_list
        except Exception as e:
            current_app.logger.critical(e)
