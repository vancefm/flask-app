import yaml
import platform
from flask import Flask
from utils.log import ConfigLogger
from utils.data_import import DataImporter

class ConfigLoader():

    def _load_config_from_yaml(app:Flask):
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

    def _load_blueprints(app:Flask):
        """Loads Flask blueprints

        Args:
            app (Flask): The current Flask app
        """
        pass
        #app.register_blueprint(error_blueprint)


    @staticmethod
    def create_app():
        app = Flask(__name__)
        ConfigLoader._load_config_from_yaml(app)
        ConfigLogger.configure_loggers(app)
        app.logger.info(f"Config loaded: {app.config.get("CUSTOM_CONFIG_PATH")}")
        # ConfigLoader._load_blueprint_config(app)
        # app.logger.info("Blueprints loaded.")

        with app.app_context():
            importer = DataImporter()
            csv_import = importer.import_csv()
        return app