
Using Python virtual environment:
1. Create virtual environment: `python -m venv .venv`
2. Activate environment, from command prompt: `.venv\Scripts\activate.bat`
    - Or from Powershell: `.venv\Scripts\Activate.ps1`

3. To install run: `pip install -r requirements.txt`

To run app: `flask run` or `flask run --debug`

Requires a config file `<hostname>.yaml`. Use `config/config-template.yaml` as an example.

Run tests: `python -m unittest discover -s tests --verbose`

Using Bootstrap 5.3.3

Flask SQlAlchemy/MySQL database