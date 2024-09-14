import yaml
import platform
from flask import Flask
from utils.log import ConfigLogger
from data.models import db
from routes.transactions import transactions_blueprint
from routes.categories import categories_blueprint
from routes.importer import importer_blueprint

class ConfigLoader():

    def _load_config_from_yaml(self, app:Flask):
        """Loads yaml config file into a Flask application. The config file
        should be named according to the hostname, and located in 'config/'

        Args:
            app (Flask): The current Flask app
        """

        # Get hostname
        hostname = platform.node()

        # Get app yaml config
        config_path = f"config/{hostname}.yaml"
        custom_config = {'CUSTOM_CONFIG_PATH': config_path}

        # Load the <hostname> YAML file
        with open(config_path, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        app.config.update(config_data)
        app.config.update(custom_config)


    def _load_blueprints(self, app:Flask):
        """Loads Flask blueprints

        Args:
            app (Flask): The current Flask app
        """

        app.register_blueprint(transactions_blueprint)
        app.register_blueprint(categories_blueprint)
        app.register_blueprint(importer_blueprint)
        app.logger.info("Blueprints loaded.")


    def _load_sqlalchemy_db(self, app:Flask):
        """Initializes SqlAlchemy, and creates missing tables

        Args:
            app (Flask): The current Flask app
        """
        with app.app_context():
            sql_uri = f"mariadb+mariadbconnector://" \
                f"{app.config['DATABASE']['USERNAME']}:" \
                f"{app.config['DATABASE']['PASSWORD']}@" \
                f"{app.config['DATABASE']['HOST']}:" \
                f"{app.config['DATABASE']['PORT']}/" \
                f"{app.config['DATABASE']['DB_NAME']}"
            app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
            db.init_app(app)
            db.create_all()
            app.logger.info("Database initiated.")

    @staticmethod
    def load_app():

        app = Flask(__name__, template_folder='../templates')

        config_loader = ConfigLoader()
        config_logger = ConfigLogger()
        
        config_loader._load_config_from_yaml(app)

        config_logger.configure_loggers(app)

        config_loader._load_blueprints(app)

        config_loader._load_sqlalchemy_db(app)

        app.logger.info(f"Config loaded: {app.config['CUSTOM_CONFIG_PATH']}")

        return app
        