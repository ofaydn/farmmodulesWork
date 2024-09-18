import time
import serial
import RPi.GPIO as GPIO

# Define the GPIO pin for RS485 DE/RE control
RS485_DE_RE_PIN = 4  # Change this to your actual pin number



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
        response = ''
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data.isprintable():
                        response = data
                        break
                except UnicodeDecodeError:
                    print("Received non-UTF-8 data, skipping...")
                    continue
            if time.time() > timeout:
                print("Response timeout.")
                break
        return response

    # Array to store measurements
    measurements = []

    # Send the 'phr' command and retrieve the first response
    send_request("phr")
    response_phr = receive_response()
    if response_phr:
        measurements.append(response_phr)

    # Wait 100 or 150 milliseconds
    time.sleep(0.15)

    # Send the 'dor' command and retrieve the second response
    send_request("dor")
    response_dor = receive_response()
    if response_dor:
        measurements.append(response_dor)

    ser.close()
    GPIO.cleanup()

    return measurements


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
            responses = data()  # Fetch the data from RS485 sensor
            if responses and len(responses) == 2:
                self.logger.debug(f"Received responses: {responses}")
                # Assuming the responses are float values
                self.value_set(0, float(responses[0]))  # Set PHR value
                self.value_set(1, float(responses[1]))  # Set DOR value
            else:
                self.logger.debug("No valid responses received or incorrect number of responses.")
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
            return None

