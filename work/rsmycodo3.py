class SensorData:
    def __init__(self, name, value=None, message=None):
        self.name = name
        self.value = value
        self.message = message

    def __repr__(self):
        return f"SensorData(name={self.name}, value={self.value}, message={self.message})"

import time
import serial
import RPi.GPIO as GPIO

# Define the GPIO pin for RS485 DE/RE control
RS485_DE_RE_PIN = 17  # Change this to your actual pin number

def data():
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in listening mode

    # Setup serial connection
    try:
        ser = serial.Serial(
            port='/dev/serial0',  # Use the correct serial port
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except serial.SerialException as e:
        print(f"Failed to connect to serial port: {e}")
        return None

    # Function to send a request
    def send_request(command):
        full_command = f'{command}\n'  # Create the full command string
        GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
        time.sleep(0.05)
        ser.write(full_command.encode('utf-8'))  # Send the command as bytes
        print(f"Request sent: '{full_command.strip()}'")
        time.sleep(0.05)
        GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

    # Function to receive the response
    def receive_response():
        timeout = time.time() + 2  # 2-second timeout
        responses = []
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        responses.append(data)
                except UnicodeDecodeError:
                    print("Received non-UTF-8 data, skipping...")
                    continue
            if time.time() > timeout:
                break
        return responses

    # Array to store sensor data
    sensor_data_list = []

    # Send the 'phr' command and retrieve the response
    send_request("phr")
    responses_phr = receive_response()
    for response in responses_phr:
        if response.replace('.', '', 1).isdigit():  # Check if response is a float
            sensor_data_list.append(SensorData(name='PHR', value=float(response)))
        else:
            sensor_data_list.append(SensorData(name='PHR', message=response))

    # Wait 150 milliseconds
    time.sleep(0.15)

    # Send the 'dor' command and retrieve the response
    send_request("dor")
    responses_dor = receive_response()
    for response in responses_dor:
        if response.replace('.', '', 1).isdigit():  # Check if response is a float
            sensor_data_list.append(SensorData(name='DOR', value=float(response)))
        else:
            sensor_data_list.append(SensorData(name='DOR', message=response))

    ser.close()
    GPIO.cleanup()

    return sensor_data_list

# Mycodo Custom Input Implementation

import copy
from mycodo.inputs.base_input import AbstractInput
#sudo apt-get -y install python3-rpi.gpio
measurements_dict = {0: {"measurement": "ion_concentration", "unit": "pH"},
                     1: {"measurement": "dissolved_oxygen", "unit": "mg_L"}}

INPUT_INFORMATION = {
    "input_name_unique": "brooooo",
    "input_manufacturer": "Ceket_Development",
    "input_name": "CKT460",
    "input_library": "RPi.GPIO",
    "measurements_name": "Ion Concentration",
    "measurements_dict": measurements_dict,
    "url_manufacturer": "https://www.microchip.com/",
    "url_datasheet": "http://ww1.microchip.com/",
    "url_product_purchase": "https://www.adafruit.com/",
    "dependencies_module": [('pip-pypi', 'RPi.GPIO','RPi.GPIO')],
    "interfaces": ["I2C"],
    "options_enabled": ["period", "pre_output"],
    "options_disabled": ["interface"],
}


class InputModule(AbstractInput):
    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)
        if not testing:
            self.initialize_input()

    def initialize_input(self):
        self.logger.debug("Initialization of RS485 Input completed.")

    def get_measurement(self):
        self.return_dict = copy.deepcopy(measurements_dict)
        try:
            sensor_data_list = data()  # Fetch the data from RS485 sensor
            if sensor_data_list:
                self.logger.debug(f"Received sensor data: {sensor_data_list}")
                # Process and set values
                for data_item in sensor_data_list:
                    if data_item.value is not None:
                        if data_item.name == 'PHR':
                            self.value_set(0, data_item.value)
                        elif data_item.name == 'DOR':
                            self.value_set(1, data_item.value)
            else:
                self.logger.debug("No valid sensor data received.")
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
            return None