import serial
import time
import RPi.GPIO as GPIO

# RS485 Direction Control Pin
RS485_DE_RE_PIN = 4

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

    # Send the command to request data
    send_request("phr")  # 'r' for the Atlas sensor

    # Receive and return the response
    response = receive_response()
    ser.close()
    GPIO.cleanup()
    return response


# Mycodo Custom Input Implementation

import copy
from mycodo.inputs.base_input import AbstractInput
#sudo apt-get -y install python3-rpi.gpio
measurements_dict = {0: {"measurement": "ion_concentration", "unit": "pH"}}

INPUT_INFORMATION = {
    "input_name_unique": "Test_RS_PH_Sensor",
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
            response = data()  # Fetch the data from RS485 sensor
            if response:
                self.logger.debug(f"Received response: {response}")
                response_value = float(response)  # Assuming the response is a float (adjust as necessary)
                self.value_set(0, response_value)
            else:
                self.logger.debug("No valid response received.")
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
            return None
