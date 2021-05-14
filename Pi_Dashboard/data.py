from flask import Blueprint, jsonify
from .sensors import  Sensors
from flask import current_app as app

data_blueprint = Blueprint("data", __name__)

@data_blueprint.route("/")
def show():
    app.logger.info("Starting to retrieve core data")
    temperature = Sensors.get_external_temps()
    
    
    
    app.logger.info("Finished retrieving core data")
    app.logger.debug(f"Core data: {temperature}")
    return jsonify(temperature)
