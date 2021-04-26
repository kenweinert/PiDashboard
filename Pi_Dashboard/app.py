import logging

from flask import Flask
from logging.handlers import RotatingFileHandler

def create_app(config_file="config/local_config.py"):
    app = Flask(__name__)  # initialize app
    app.config.from_pyfile(config_file, silent=False) # read in config from file
    
    # Configure file-base log handler
    log_file_handler = RotatingFileHandler(filename=app.config.get("LOG_FILE_NAME", "config/pi-dashboard.log"), maxBytes=10000000,backupCount=4)
    log_file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(messages"))
    app.logger.addHandler(log_file_handler)
    app.logger.setLevel(app.config.get("LOGGER_LEVEL", "ERROR"))
    app.logger.info("----- STARTING APP -----")
    @app.route("/")
    
    def hello_world():
        app.logger.info("Running first route")
        return "Hello, World!"
    
    app.logger.info("----- FINISHED STARTING APP -----")
    return app;

    