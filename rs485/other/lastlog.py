import serial
import RPi.GPIO as GPIO
from datetime import datetime
import time

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
    print(f"Failed to connect to serial port: {e}")
    raise

log_file_path = 'sensor_data_log.csv'

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
        print(f"Data error: {ve}")
    except serial.SerialTimeoutException:
        print("Timeout: No data received from sensor")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        GPIO.output(4, GPIO.HIGH)  # Ensure GPIO4 is HIGH for idle state
    return None

# Open the log file in append mode
with open(log_file_path, 'a') as log_file:
    while True:
        temperature = read_temperature()
        if temperature is not None:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{current_time},{temperature}\n"
            log_file.write(log_entry)
            print(f"{current_time} - Temperature: {temperature}°C")
        time.sleep(1)  # Delay between readings
