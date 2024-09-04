import random
import copy

from mycodo.inputs.base_input import AbstractInput

def count_lines(filename):
    """
    Function that counts the number of lines within the given file name
    """
    with open(filename, 'r') as f:
        return sum(1 for _ in f)

    
    
def get_random_line(filename, num_lines):
        """
        Function that returns a random line from data file.
        If can't retrieve any data simply returns -1
        """
        line_number = random.randint(0, num_lines - 1)
        with open(filename, 'r') as f:
            for current_line_number, line in enumerate(f):
                if current_line_number == line_number:
                    return line.strip()
                
filename = '/home/raspberry/Mycodo/mycodo/utils/data2.txt'
num_lines = count_lines(filename)
# Measurements
measurements_dict = {
    0: {
        'measurement': 'temperature',
        'unit': 'C'
    }
}

# Input information
INPUT_INFORMATION = {
    'input_name_unique': 'Test Text Sensor4',
    'input_manufacturer': 'Ceket Development4',
    'input_name': 'CKT115',
    'input_library': '',
    'measurements_name': 'Temperature',
    'measurements_dict': measurements_dict,
    'url_manufacturer': 'https://www.microchip.com/wwwproducts/en/en556182',
    'url_datasheet': 'http://ww1.microchip.com/downloads/en/DeviceDoc/MCP9808-0.5C-Maximum-Accuracy-Digital-Temperature-Sensor-Data-Sheet-DS20005095B.pdf',
    'url_product_purchase': 'https://www.adafruit.com/product/1782',

    'dependencies_module': [],

    'interfaces': ['I2C'],
    'i2c_location': ['0x64','0x65'],
    'i2c_address_editable': True,

    'options_enabled': [
        'i2c_location',
        'period',
        'pre_output'
    ],
    'options_disabled': ['interface']
}


class InputModule(AbstractInput):
    """
    Inherits class for designing a custom input from MyCodo's library.
    """
    def __init__(self, input_dev, testing=False):
        """
        Function for initializing the input.
        """
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)
        self.sensor = None
        if not testing:
            self.initialize_input()

    def initialize_input(self):
        """
        Initializing function
        """
        print("Init function")
    def get_measurement(self):
        """
        Function to get the measurements from the sensor.
        """
        self.return_dict = copy.deepcopy(measurements_dict)
        try:
            temperature_c = get_random_line(filename, num_lines)
            self.logger.debug(f"Value returned from the sensor library: {temperature_c}. Saving to database.".format(temperature_c))
            self.value_set(0, temperature_c)
            return self.return_dict
        except Exception as msg:
            self.logger.exception("Input read failure: {}".format(msg))