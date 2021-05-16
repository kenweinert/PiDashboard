from flask import current_app as app
from gpiozero import Button, exc
from builtins import staticmethod

try:
    from w1thermsensor  import W1ThermSensor
except Exception:
    W1ThermSensor = None
    
class Sensors:
    @staticmethod
    def get_external_temps():
        """
        Safely read the external temperature
        :return: Integer of current temperature
        """
        app.logger.info("Starting to read temperature sensor")
        temp = "{:.2f}"
        temperature = {}
        try:
            for sensor in W1ThermSensor.get_available_sensors():
                temperature [sensor.id] = temp.format(sensor.get_temperature())
        except TypeError as e:
            app.logger.warning(f"Unable to use primary temperature sensor in this environment: {e}")
            temperature = 0
        except Exception as e:
            app.logger.error(f"Unknown problem with primary external temperature sensor: {e}")
            temperature = 0
        
        app.logger.info("Finished reading temperature sensor")
        app.logger.debug(f"Temperature: {temperature}")
        return temperature

    @staticmethod
    def get_trunk_status():
        """
        Safely read the trunk sensor and calculate the state:
        Open, Closed, Unknown
        :return: String - trunk status
        """
        app.logger.info("Starting to read the trunk sensor")
        result = None
        status = None
        
        try:
            button = Button(pin=14)
            status = button.is_pressed
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use the trunk sensor in this environment: {e}")
            result = "Unknown"
        except Exception as e:
            app.logger.error(f"Unknown problem with trunk sensor: {e}")
            result = "Unknown"
            
        if not result:
            if status:
                result = "Closed"
            else:
                result = "Open"
                
        app.logger.debug(f"Trunk: {result}")
        app.logger.info("Finished reading trunk sensor")
        
        return result           