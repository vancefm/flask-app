from flask import current_app
import pandas

class DataImporter:

    def __init__(self):
        self.csv_data_path = f"{current_app.config['DATA']['DATA_IMPORT_PATH']}"

    def import_csv(self):
        try:
            csv_dataframe = pandas.read_csv(self.csv_data_path, index_col=False)
            print(csv_dataframe)
            return csv_dataframe
        except Exception  as e:
            current_app.logger.critical(e)