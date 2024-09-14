from flask import current_app, request, render_template
from utils.errors.error_handler import handle_errors
from utils.config_loader import ConfigLoader


app = ConfigLoader.load_app()

@app.before_request
def request_logger():
    """ Log each request as it comes in
    """
    current_app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route("/")
@handle_errors
def root_route():
    return render_template("test.html")

if __name__ == '__main__':
    app.run()