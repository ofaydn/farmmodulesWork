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

    def send_command(self, command):
        full_command = f'{command}\n'
        GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)
        time.sleep(0.05)
        ser.write(full_command.encode('utf-8'))
        time.sleep(0.05)
        GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)

    def read_response(self):
        time.sleep(0.1)
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8', errors='ignore').strip()
            if message:
                return message
        return None


def verify_arduino():
    send_request("sla1_verify")

    time.sleep(0.1)
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Raw response: {response}")  # Print the raw response to debug

        try:
            data = json.loads(response)  # Attempt to parse the JSON
            print(f"Parsed JSON: {data}")  # Print the parsed data
            if data.get("verify"):
                return ArduinoDevice("sla1", data.get("sensors"))
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
    return None


def send_request(command):
    full_command = f'{command}\n'
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)


try:
    while True:
        command = input("Enter command pls: ")
        if command == "verify":
            arduino = verify_arduino()
            if arduino:
                print(f"Arduino {arduino.name} connected with sensors: {arduino.sensors}")
            else:
                print("Arduino not verified.")
        else:
            send_request(command)

except KeyboardInterrupt:
    ser.close()
    GPIO.cleanup()
