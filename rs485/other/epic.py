import serial
import RPi.GPIO as GPIO
from datetime import datetime
import logging
import time

# Setup logging
logging.basicConfig(filename='sensor_errors.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

# GPIO setup for RS485 control
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO4 as output for RS485 DE/RE control

# Initialize the serial connection
try:
    ser = serial.Serial(
        port='/dev/serial0',
        baudrate=9600,
        timeout=1
    )
except serial.SerialException as e:
    logging.error(f"Failed to connect to serial port: {e}")
    raise

def read_temperature():
    try:
        GPIO.output(4, GPIO.LOW)  # Set GPIO4 to LOW for receiving data
        time.sleep(0.01)  # Small delay to ensure the line is stable

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            GPIO.output(4, GPIO.HIGH)  # Set GPIO4 to HIGH after reading
            if data:
                return float(data)
            else:
                raise ValueError("Received empty data from sensor")
    except ValueError as ve:
        logging.error(f"Data error: {ve}")
    except serial.SerialTimeoutException:
        logging.warning("Timeout: No data received from sensor")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        GPIO.output(4, GPIO.HIGH)  # Ensure GPIO4 is HIGH for idle state
    return None

while True:
    temperature = read_temperature()
    if temperature is not None:
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"{current_time} - Temperature: {temperature}°C")
