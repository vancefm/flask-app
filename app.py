from flask import Flask, request
from util.config_loader import ConfigLoader

app = ConfigLoader.create_app()

@app.before_request
def request_logger():
    app.logger.info(f"{request.remote_addr} {request.method} {request.path}")

@app.route("/")
def hello_world():
    app.logger.info("Root route accessed.")
    app.logger.debug("Root route debug accessed.")
    app.logger.error("Root route error accessed.")
    return "<p>Flask App loaded.</p>"

if __name__ == '__main__':
    app.run()