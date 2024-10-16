import minimalmodbus
import RPi.GPIO as GPIO
import time

RE_DE_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RE_DE_PIN, GPIO.OUT)

# Adjust the port if necessary
instrument = minimalmodbus.Instrument('/dev/serial0', 1)
instrument.serial.baudrate = 19200
instrument.serial.timeout = 2.0
instrument.debug = True

def set_re_de_pin(state):
    GPIO.output(RE_DE_PIN, state)
    time.sleep(0.1)

def read_ky028():
    try:
        set_re_de_pin(GPIO.HIGH)  # Set to transmit mode
        time.sleep(0.1)
        print("Requesting KY-028 value from Arduino...")
        ky028_value = instrument.read_register(0, 0)  # Adjust register if needed
        set_re_de_pin(GPIO.LOW)  # Set to receive mode
        print(f"KY-028 value from Arduino: {ky028_value}")
    except Exception as e:
        print(f"An error occurred while reading KY-028: {str(e)}")

if __name__ == '__main__':
    while True:
        read_ky028()
        time.sleep(5)
