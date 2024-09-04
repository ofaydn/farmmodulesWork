"""Custom input that retrieves data from a given text file."""

import copy
import serial


from mycodo.inputs.base_input import AbstractInput

# Measurements
measurements_dict = {0: {"measurement": "temperature", "unit": "C"}}

def get_data():
    ser = serial.Serial(
    port='/dev/serial0',
    baudrate=19200,
    timeout=1
    )

    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf8').strip()
            if data:
                return data
            else:
                # Handle case where data is empty after strip
                return "No data received"
        else:
            # Handle case where no data is available
            return "No data available"
    except Exception as e:
        # Log or handle the exception
        print(f"Error occurred: {e}")
        return None

# Input information
INPUT_INFORMATION = {
    "input_name_unique": "RS485 Temperature",
    "input_manufacturer": "Ceket Development",
    "input_name": "CKT243",
    "input_library": "serial",
    "measurements_name": "Temperature",
    "measurements_dict": measurements_dict,
    "url_manufacturer": "https://www.microchip.com/wwwproducts/en/en556182",
    "url_datasheet": "http://ww1.microchip.com/downloads/en/DeviceDoc/MCP9808-0.5C-Maximum-Accuracy-Digital-Temperature-Sensor-Data-Sheet-DS20005095B.pdf",
    "url_product_purchase": "https://www.adafruit.com/product/1782",
    "dependencies_module": [],
    "interfaces": ["I2C"],
    "i2c_location": ["0x64", "0x65"],
    "i2c_address_editable": True,
    "options_enabled": ["i2c_location", "period", "pre_output"],
    "options_disabled": ["interface"],
}


class InputModule(AbstractInput):
    """Inherits class for designing a custom input from MyCodo's library."""

    def __init__(self, input_dev, testing=False):
        """Function for initializing the input."""
        super().__init__(input_dev, testing=testing, name=__name__)
        self.sensor = None
        if not testing:
            self.initialize_input()

    def initialize_input(self):
        """Initializing function."""
        print("Init function")

    def get_measurement(self):
        """Function to get the measurements from the sensor."""
        self.return_dict = copy .deepcopy(measurements_dict)
        try:
            data = get_data()
            temperature_c = float(data)
            self.logger.debug(f"Value returned from the sensor library: {temperature_c}. Saving to database.")
            self.value_set(0, temperature_c)
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
