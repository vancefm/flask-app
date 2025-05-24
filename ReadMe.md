# Financinator

## Starting the app

Using Python virtual environment:
1. Create virtual environment: `python -m venv .venv`
2. Activate environment, from command prompt: `.venv\Scripts\activate.bat`
    - Or from Powershell: `.venv\Scripts\Activate.ps1`

3. To install run: `pip install -r requirements.txt`

To run app: `flask run` or `flask run --debug`

Requires a config file `<hostname>.yaml`. Use `config/config-template.yaml` as an example.
Requires a categories file `categories.yaml`. Use `config/categories-template.yaml` as an example.

Run tests: `python -m unittest discover -s tests --verbose`

Using Bootstrap 5.3.3
Using Flask SQlAlchemy/MySQL database

## Categories

### Category configuration

Categories are configured using a `categories.yaml` file. You can checkout the `config/categories-template.yaml` file for reference. Categories configured in this file are automatically imported into the database at startup. Existing categries are skipped.

Categories are designed using a 1-to-many pattern, where a given category may have multiple sub-cateogories. Categories and sub-categories may have the same name. However, the database enforces uniqueness for a combination of parent category and category name. For example, you may not create two parent categories with the same name, or two sub-categories with the same name which have the same parent.

## Transactions

### Data import

Transactions may be imported using a CSV file. A list of required CSV headers can be found in the main configuration file in the DATA:CSV_HEADERS section. It is not recommended to change these fields, as the code depends on these values.