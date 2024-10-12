# UNDER MIT LICENSE
# created by Muhammed Çağrı KÜÇÜKALP 11.10.2024 hope it will help you achieve something well. 
# This Python code establishes a serial RS485 communication between Raspberry Pi and a connected device.
# The GPIO pin 4 is used for RS485 direction control (switching between transmit and receive modes).
# It reads data from the RS485 bus via the specified serial port ('/dev/serial0') and prints the received message to the console.

import serial
import RPi.GPIO as GPIO
import time

# RS485 direction control pin
RS485_DE_RE_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)

# Serial port setup
ser = serial.Serial(
    port='/dev/serial0',  # Use the correct serial port for your Raspberry Pi
    baudrate=9600,        # RS485 baud rate set to 9600
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Start in listening mode (receive)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)

print("RS485 Communication Test Started...")

try:
    while True:
        if ser.in_waiting > 0:  # If data is available
            try:
                # Read and decode the incoming message
                message = ser.readline().decode('utf-8', errors='ignore').strip()
                if message:
                    print(f"Received message: {message}")
            except UnicodeDecodeError as e:
                print(f"Data decoding error: {e}")
        # Wait for 1 second before next loop iteration
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial port and clean up GPIO settings
    ser.close()
    GPIO.cleanup()
