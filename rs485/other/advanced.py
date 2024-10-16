import serial
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

# Set up GPIO pins
RE_DE_PIN = 12  # GPIO pin connected to RE/DE
GPIO.setmode(GPIO.BCM)
GPIO.setup(RE_DE_PIN, GPIO.OUT)

# Function to set RS485 to receive mode
def set_receive_mode():
    GPIO.output(RE_DE_PIN, GPIO.LOW)

# Function to set RS485 to transmit mode
def set_transmit_mode():
    GPIO.output(RE_DE_PIN, GPIO.HIGH)

# Open the serial port with appropriate settings
ser = serial.Serial(
    port='/dev/serial0',  # This is the primary UART (TXD0/RXD0 on GPIO14/15)
    baudrate=9600,
    timeout=1
)

# Time offset (e.g., 7 seconds)
time_offset = timedelta(seconds=7)

try:
    while True:
        set_receive_mode()  # Set to receive mode
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # Get current time and apply offset
            current_time = datetime.now() - time_offset
            formatted_time = current_time.strftime('%H:%M:%S')
            print(f"{formatted_time} - Temperature: {data}°C")
finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
