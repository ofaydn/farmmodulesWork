import copy
import serial
import RPi.GPIO as GPIO
import time

RS485_DE_RE_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)

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
    exit(1)

from mycodo.inputs.base_input import AbstractInput


def send_request(slave_id):
    command = f'S{slave_id}_A\n'  # Create the command string
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(command.encode('utf-8'))  # Send the command as bytes
    print(f"Request sent: '{command.strip()}'")
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW) 

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



# Measurements
measurements_dict = { 0 : {"measurement": "ion_concentration", "unit":"pH"}}


# Input information
INPUT_INFORMATION = {
    "input_name_unique": "Test_RS_Sensor",
    "input_manufacturer": "Ceket_Development",
    "input_name": "CKT460",
    "input_library": "RPi",
    "measurements_name": "Temperature",
    "measurements_dict": measurements_dict,
    "url_manufacturer": "https://www.microchip.com/wwwproducts/en/en556182",
    "url_datasheet": "http://ww1.microchip.com/downloads/en/DeviceDoc/MCP9808-0.5C-Maximum-Accuracy-Digital-Temperature-Sensor-Data-Sheet-DS20005095B.pdf",
    "url_product_purchase": "https://www.adafruit.com/product/1782",
    "dependencies_module": ["pip-pypi","RPi","RPi"],
    "interfaces": ["I2C"],
    "i2c_location": ["0x64", "0x65"],
    "i2c_address_editable": True,
    "options_enabled": ["i2c_location", "period", "pre_output"],
    "options_disabled": ["interface"],
}


class InputModule(AbstractInput):
    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)
        self.sensor = None
        if not testing:
            self.initialize_input()

    def initialize_input(self):
        print("Init function")

    def get_measurement(self):
        self.return_dict = copy.deepcopy(measurements_dict)
        try:
            send_request(1)
            response = receive_response()
            if response:
                print(f"Received response: {response}")
            else:
                print("No valid response received.")
            self.logger.debug(f"Value returned from the sensor library: {response}. Saving to database.")
            self.value_set(0, response)
            ser.close()
            GPIO.cleanup()
            return self.return_dict
        except Exception as msg:
            self.logger.exception(f"Input read failure: {msg}")
