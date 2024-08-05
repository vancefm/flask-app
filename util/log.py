from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import logging


class ConfigLogger():

    def _configure_file_logger(self, app:Flask):
        filehandler = RotatingFileHandler(
            app.config['LOG']['LOG_PATH'],
            maxBytes=app.config['LOG']['LOG_MAX_BYTES'],
            backupCount=app.config['LOG']['LOG_RETENTION_COUNT'])
        
        formatter = logging.Formatter(app.config['LOG']['LOG_FORMAT'])

        filehandler.setFormatter(formatter)

        # Set debug mode, per config
        if app.config['LOG']['LOG_DEBUG_MODE']:
            filehandler.setLevel(logging.DEBUG)
        else:
            filehandler.setLevel(logging.INFO)
        
        app.logger.addHandler(filehandler)

    def _configure_default_logger(self, app:Flask):
        # Set debug mode, per config
        if app.config['LOG']['LOG_DEBUG_MODE']:
            app.logger.setLevel(logging.DEBUG)
        else:
            app.logger.setLevel(logging.INFO)

    @staticmethod
    def configure_loggers(app:Flask):

        config_logger = ConfigLogger()
        
        config_logger._configure_file_logger(app)
        config_logger._configure_default_logger(app)
        
        # Remove the default flask log handler
        app.logger.removeHandler(default_handler)
        
        app.logger.info("Loggers configured.")
        