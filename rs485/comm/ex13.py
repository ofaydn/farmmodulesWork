# UNDER MIT LICENSE
# created by Muhammed Çağrı KÜÇÜKALP 11.10.2024 hope it will help you achieve something well. 
# This Python code establishes a serial RS485 communication between Raspberry Pi and a connected device.
# The GPIO pin 4 is used for RS485 direction control (switching between transmit and receive modes).
# It reads data from the RS485 bus via the specified serial port ('/dev/serial0') and prints the received message to the console.
# Allows sending any command from the Raspberry Pi to connected devices via RS485.

import serial
import RPi.GPIO as GPIO
import time
import threading

# RS485 direction control pin
RS485_DE_RE_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)

# Serial port setup
ser = serial.Serial(
    port='/dev/serial0',  # Serial port for Raspberry Pi
    baudrate=9600,        # RS485 baud rate set to 9600
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Start in listening mode (receive)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)

print("RS485 Communication Test Started...")

def send_data(data):
    """Send data over RS485."""
    try:
        # Switch to transmit mode
        GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)
        ser.write((data + '\n').encode('utf-8'))  # Ensure new line is sent as part of the message
        ser.flush()  # Ensure all data is sent
        print(f"Sent message: {data}")
    except Exception as e:
        print(f"Failed to send data: {e}")
    finally:
        # Switch back to receive mode
        time.sleep(0.1)  # Ensure transmit completes before switching to receive
        GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)

def send_request(command):
    full_command = f'{command}\n'
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))  # Send the command
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

#def ask_user_to_send():
#    """Prompt user to send data every 3 seconds."""
#    while True:
#        time.sleep(3)  # Wait for 3 seconds
#        message_to_send = input("Enter the command to send: ")
#        send_data(message_to_send)

# Start a thread to handle user input and sending data
#send_thread = threading.Thread(target=ask_user_to_send)
#send_thread.daemon = True  # Daemonize thread to exit with the program
#send_thread.start()
count = 0;

try:
    while True:
        # Check if there's incoming data
       # if ser.in_waiting > 0:  # If data is available
       #     try:
       #         # Read and decode the incoming message
       #         message = ser.readline().decode('utf-8', errors='ignore').strip()
       #         if message:
       #             print(f"Received message: {message}")
       #     except UnicodeDecodeError as e:
       #         print(f"Data decoding error: {e}")
        # Sleep for a short time to reduce CPU usage
        send_request(count)
        time.sleep(0.5)
        count+=1

except KeyboardInterrupt:
    # Close the serial port and clean up GPIO settings
    ser.close()
    GPIO.cleanup()

