import serial
import RPi.GPIO as GPIO
import time

RS485_DE_RE_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in receive mode

def send_request(command):
    full_command = f'{command}\n'
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))  # Send the command
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to receive mode

try:
    while True:
        command = input("Enter command pls: ")
        send_request(command)

        # Check for response
        time.sleep(0.1)
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8', errors='ignore').strip()
            if message:
                print(f"Received message: {message}")

except KeyboardInterrupt:
    ser.close()
    GPIO.cleanup()
