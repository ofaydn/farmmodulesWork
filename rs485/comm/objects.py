import serial
import RPi.GPIO as GPIO
import time
import json

RS485_DE_RE_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in receive mode

class ArduinoDevice:
    def __init__(self, name, sensors):
        self.name = name
        self.sensors = sensors

    def __repr__(self):
        return f"Device: {self.name}, Sensors: {', '.join(self.sensors)}"

connected_devices = []  # List to store connected devices

def send_request(command):
    full_command = f'{command}\n'
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))  # Send the command
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to receive mode

def verify_arduino():
    send_request("sla1_verify")
    time.sleep(0.2)  # Slightly increase the wait time

    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Raw response: {response}")  # Print raw response for debugging

        try:
            data = json.loads(response)  # Try to parse the JSON response
            print(f"Parsed JSON: {data}")  # Print the parsed JSON
            if data.get("verify"):
                device = ArduinoDevice("sla1", data.get("sensors"))
                connected_devices.append(device)  # Add to connected devices list
                print(f"Arduino verified: {device}")
                return device
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
    return None

def list_devices():
    if connected_devices:
        print("Currently connected devices:")
        for device in connected_devices:
            print(f"Device: {device.name}")
            print("Sensors:")
            for sensor in device.sensors:
                print(f"  - {sensor}")
    else:
        print("No devices are currently connected.")

try:
    while True:
        command = input("Enter command pls: ")

        if command == "verify":
            device = verify_arduino()
            if device:
                print(f"{device.name} connected.")
            else:
                print("Arduino not verified.")
        
        elif command == "list_devices":
            list_devices()

        else:
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
