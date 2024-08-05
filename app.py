from flask import Flask
from util.config_loader import ConfigLoader

app = ConfigLoader.create_app()

@app.route("/")
def hello_world():
    app.logger.info("Root route accessed.")
    app.logger.debug("Root route debug accessed.")
    return "<p>Flask App loaded.</p>"

if __name__ == '__main__':
    app.run()