from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler, SMTPHandler
import logging
from utils.request_filter import RequestIdFilter


class ConfigLogger():

    def _configure_default_logger(self, app:Flask):

        app.logger.addFilter(RequestIdFilter())

        # Set debug mode, per config
        if app.config['LOG']['LOG_DEBUG_MODE']:
            app.logger.setLevel(logging.DEBUG)
        else:
            app.logger.setLevel(logging.INFO)

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

    def _configure_error_file_logger(self, app:Flask):
        error_filehandler = RotatingFileHandler(
            app.config['LOG']['ERROR_LOG_PATH'],
            maxBytes=app.config['LOG']['LOG_MAX_BYTES'],
            backupCount=app.config['LOG']['LOG_RETENTION_COUNT'])
        
        formatter = logging.Formatter(app.config['LOG']['LOG_FORMAT'])

        error_filehandler.setFormatter(formatter)

        error_filehandler.setLevel(logging.ERROR)
        
        app.logger.addHandler(error_filehandler)

    def _configure_error_smtp_logger(self, app:Flask):

        # If email notifications are disabled, we can return
        if not app.config['EMAIL']['ENABLED']:
            return

        # Collect any credentials to use
        if (app.config['EMAIL']['USERNAME'] and
            app.config['EMAIL']['PASSWORD']):
            cred_dict = {app.config['EMAIL']['USERNAME'], app.config['EMAIL']['PASSWORD']}
        else:
            cred_dict = None

        # Collect any secure files' paths
        if (app.config['EMAIL']['SECURE_KEY'] and
            app.config['EMAIL']['SECURE_CERT']):
            secure_dict = {app.config['EMAIL']['SECURE_KEY'], app.config['EMAIL']['SECURE_CERT']}
        else:
            secure_dict = None

        smtp_handler = SMTPHandler(
            mailhost=(app.config['EMAIL']['HOST'], app.config['EMAIL']['PORT']),
            fromaddr=app.config['EMAIL']['FROM_ADDR'],
            toaddrs=app.config['EMAIL']['ADMIN_EMAIL'],
            subject=app.config['EMAIL']['NOTIFY_SUBJECT'],
            credentials=(cred_dict),
            secure=(secure_dict),
            timeout=app.config['EMAIL']['TIMEOUT'])
        
        formatter = logging.Formatter(app.config['LOG']['LOG_FORMAT'])
        smtp_handler.setFormatter(formatter)
        smtp_handler.setLevel(logging.ERROR)

        app.logger.addHandler(smtp_handler)


    @staticmethod
    def configure_loggers(app:Flask):

        config_logger = ConfigLogger()
        
        config_logger._configure_default_logger(app)
        config_logger._configure_file_logger(app)
        config_logger._configure_error_file_logger(app)
        
        # Remove the default flask log handler
        app.logger.removeHandler(default_handler)
        
        app.logger.info("Loggers configured.")
        