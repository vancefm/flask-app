from flask import current_app, request, render_template
from utils.errors.error_handler import handle_errors
from utils.config_loader import ConfigLoader
from utils.errors.custom_exception import CustomException


app = ConfigLoader.create_app()

@app.before_request
def request_logger():
    """ Log each request as it comes in
    """
    current_app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route("/")
@handle_errors
def root_route():
    current_app.logger.info("Root route accessed.")
    current_app.logger.debug("Root route debug accessed.")
    current_app.logger.warning("Root route warning accessed.")
    current_app.logger.error("Root route error accessed.")
    current_app.logger.critical("Root route critical accessed.")

    return "<p>Root route</p>"

@app.errorhandler(CustomException)
def error_page(e):
    return "<p>Root route error: custom</p>", 500

@app.errorhandler(Exception)
def error_page(e):
    return "<p>Root route error</p>", 500

if __name__ == '__main__':
    app.run()