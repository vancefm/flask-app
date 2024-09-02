from flask import current_app
import pandas
import yaml
from data.models.transaction import Transaction
from data.models.category import Category

class DataImporter:
    """Initializes with transactions from TX_IMPORT_PATH, and categories
    from CATEGORIES_LIST_PATH
    """

    def __init__(self):
        self.csv_data_path = f"{current_app.config['DATA']['TX_IMPORT_PATH']}"
        self.transaction_list = []
        self.category_list = []
        self.pattern_dict = {}
        self._import_transactions_csv()


    def _import_transactions_csv(self):
        """Import a CSV transaction file

        Returns:
            List: A list of transactions.
        """
        try:
            csv_dataframe = pandas.read_csv(self.csv_data_path, index_col=False)
            
            self.category_list = self._import_categories_from_yaml()
            self.pattern_dict = self._get_pattern_categories()
            
            self.transaction_list = csv_dataframe.apply(
                lambda row: 
                Transaction(
                    row['Posting Date'], 
                    row['Description'], 
                    row['Amount'],
                    row['Type'],
                    row['Balance']), axis=1).tolist()
            
            current_app.logger.debug(f"Transactions imported from {self.csv_data_path}")
            pattern: str
            tx: Transaction
            for tx in self.transaction_list:
                for pattern in self.pattern_dict:
                    if pattern in tx.description :
                        tx.category_name = self.pattern_dict.get(pattern)
            current_app.logger.debug("Transactions categorized.")
            return self.transaction_list
        except Exception as e:
            current_app.logger.critical(e)

    def _import_categories_from_yaml(self):
        """Load categories yaml file

        Returns:
            category_list(List): A List of the categories and their match patterns
        """
        try:
            # Get categories from file
            with current_app.app_context():
                categories_path = current_app.config['DATA']['CATEGORIES_LIST_PATH']
                with open(categories_path, 'r') as cat_file:
                    cat_data = yaml.safe_load(cat_file)
                    current_app.logger.debug(f"Loaded file: {categories_path}")

                    # Create a list of all categories
                    cat_list = []
                    for category in cat_data['Categories']:
                        # The list of subcategories is automatically created via the Category constructor
                        c = Category(
                            category['name'], 
                            category['match_patterns'],
                            category['subcategories'])
                        cat_list.append(c)
                    current_app.logger.debug(f"Categories imported from: {categories_path}")
                    current_app.logger.debug(cat_list)
                return cat_list
        except Exception as e:
            current_app.logger.critical(e)
    
    def _get_pattern_categories(self):
        """Collects a dict of patterns and their corresponding categories.

        Returns:
            dict: A dictionary of patterns and categories
        """
        pattern_dict = {}
        if self.category_list.count != 0:
            category: Category
            for category in self.category_list:
                cat_name = category.name

                # Get patterns for top level categories                
                for pattern in category.match_patterns:
                    pattern_dict.update({pattern : cat_name})

                # Get patterns for sub categories
                sub_cat: SubCategory
                for sub_cat in category.subcategories:
                    sub_name = sub_cat.name
                    for sub_pattern in sub_cat.match_patterns:
                        long_cat = f"{cat_name}: {sub_name}"
                        pattern_dict.update({sub_pattern : long_cat})
            current_app.logger.debug("Category patterns imported.")
            current_app.logger.debug(pattern_dict)
        return pattern_dict
