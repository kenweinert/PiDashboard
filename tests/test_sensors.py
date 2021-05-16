from unittest.mock import patch
from Pi_Dashboard.sensors import Sensors
from gpiozero import exc


class TestSensors:
    @patch("Pi_Dashboard.sensors.Button")
    def test_get_trunk_status_bad_pin_factory(self, mock_button):
        mock_button.side_effect = exc.BadPinFactory
        result = Sensors.get_trunk_status()
        assert result == "Unknown"

    @patch("Pi_Dashboard.sensors.Button")
    def test_get_trunk_status_other_pin_error(self, mock_button):
        mock_button.side_effect = TypeError
        result = Sensors.get_trunk_status()
        assert result == "Unknown"

    @patch("Pi_Dashboard.sensors.Button")
    def test_get_trunk_status_closed(self, mock_button):
        mock_button.return_value = type("Button", (), {"is_pressed": True})
        result = Sensors.get_trunk_status()
        assert result == "Closed"

    @patch("Pi_Dashboard.sensors.Button")
    def test_get_trunk_status_open(self, mock_button):
        mock_button.return_value = type("Button", (), {"is_pressed": False})
        result = Sensors.get_trunk_status()
        assert result == "Open"
