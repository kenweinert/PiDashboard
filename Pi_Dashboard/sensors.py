from flask import current_app as app
from gpiozero import Button, exc, LightSensor
from builtins import staticmethod

try:
    from w1thermsensor import W1ThermSensor
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
                temperature[sensor.id] = temp.format(sensor.get_temperature())
        except TypeError as e:
            app.logger.warning(
                f"Unable to use primary temperature sensor in this environment: {e}"
            )
            temperature = 0
        except Exception as e:
            app.logger.error(
                f"Unknown problem with primary external temperature sensor: {e}"
            )
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
            app.logger.warning(
                f"Unable to use the trunk sensor in this environment: {e}"
            )
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

    @staticmethod
    def get_light_status():
        """
        Safely read the light and calculate a status
        Daytime/Dusk/Nighttime/Unknown
        :return: String - light status
        """
        app.logger.info("Starting to read available light")
        status = -1

        try:
            sensor = LightSensor(pin=15)
            status = float(sensor.value)
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use light sensor in this environment: {e}")
        except Exception as e:
            app.logger.error(f"Unknown problem with light sensor {e}")

        if status == -1:
            result = "Unknown"
        elif status >= 0.5:
            result = "Daytime"
        else:
            result = "Nighttime"

        app.logger.debug(f"Light: {status} - {result}")
        app.logger.info("Finished reading available light")

        return result
