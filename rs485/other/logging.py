import serial
import RPi.GPIO as GPIO
from datetime import datetime

# Set up GPIO for RS485 DE/RE control
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO4 as output for RS485 DE/RE control

# Set up serial communication
ser = serial.Serial(
    port='/dev/serial0',  
    baudrate=9600,
    timeout=1
)

# Define the path for the log file
log_file_path = 'sensor_data_log.csv'

try:
    # Open the log file in append mode
    with open(log_file_path, 'a') as log_file:
        while True:
            if ser.in_waiting > 0:
                try:
                    GPIO.output(4, GPIO.HIGH)  # Enable transmission
                    data = ser.readline().decode('utf-8').strip()
                    GPIO.output(4, GPIO.LOW)   # Disable transmission
                    
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Log data to the file
                    log_file.write(f"{current_time},{data}\n")
                    
                    print(f"{current_time} - Temperature: {data}°C")
                    
                except Exception as e:
                    print(f"Data error: {e}")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()
