from flask import current_app as app
from gpiozero import Button, exc, LightSensor, MCP3008
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
    def get_bool_pin(input_pin, pull_up_value):
        """
        Defensively read boolean pin as a button
        :param pin: GPIO pin (in BCM layout) to read
        :return: Boolean result -- pressed, not pressed, None
        """
        app.logger.info(f"Starting to read boolean value from pin: {input_pin}")

        try:
            button = Button(pin=input_pin, pull_up=pull_up_value)
            result = button.is_pressed
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use pin sensor in this environment: {e}")
            result = None
        except Exception as e:
            app.logger.error(f"Unknown problem with pin sensor: {e}")
            result = None

        app.logger.info(f"Finished reading boolean value from pin: {input_pin}/{result}")

        return result

    @classmethod
    def get_trunk_status(cls):
        """
        Safely read the trunk sensor and calculate the state - open/closed/unavailable/unknown
        :return: String - trunk status
        """
        app.logger.info("Starting to read the trunk sensor")
        button_status = cls.get_bool_pin(input_pin=14, pull_up_value=True)
        if button_status is None:
            result = "Unknown"
        else:
            if button_status:
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
            sensor = MCP3008(channel=0)
            status = 3.3 * sensor.value
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
