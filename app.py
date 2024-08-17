from flask import Flask, request
from util.config_loader import ConfigLoader
from util.errors.error_handler import handle_errors, CustomException

app = ConfigLoader.create_app()

@app.before_request
def request_logger():
    app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route("/")
def root_route():
    app.logger.info("Root route accessed.")
    app.logger.debug("Root route debug accessed.")
    app.logger.error("Root route error accessed.")
    app.logger.warning("Root route warning accessed.")
    return "<p>Flask App loaded.</p>"

@handle_errors
@app.route("/err")
def error_route():
    raise CustomException("Message stuff", ['Error1', 'Error2'])

if __name__ == '__main__':
    app.run()