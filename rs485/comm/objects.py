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

device_list = ["sla1", "sla2", "slb3", "slb4"]  # Example device list
connected_devices = {}

class ArduinoDevice:
    def __init__(self, device_id, sensors):
        self.device_id = device_id
        self.sensors = sensors

    def get_sensors(self):
        return self.sensors

    def __str__(self):
        return f"Arduino {self.device_id} with sensors: {', '.join(self.sensors)}"

def send_request(command):
    full_command = f'{command}\n'
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))  # Send the command
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to receive mode

def verify_device(device_id, timeout=1):
    send_request(f'{device_id}_verify')
    start_time = time.time()
    while time.time() - start_time < timeout:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8', errors='ignore').strip()
            if message:
                print(f"Received message: {message}")
                if '{"verify":true' in message:
                    sensors = eval(message).get('sensors', [])
                    connected_devices[device_id] = ArduinoDevice(device_id, sensors)
                    print(f"{device_id} verified with sensors: {sensors}")
                    return True
        time.sleep(0.1)  # Polling delay
    return False

def verify_all_devices():
    for device_id in device_list:
        if verify_device(device_id):
            print(f"{device_id} is connected.")
        else:
            if device_id in connected_devices:
                del connected_devices[device_id]  # Remove device if not verified
            print(f"{device_id} not connected or verification failed.")

def list_devices():
    if connected_devices:
        print("Currently connected devices and their sensors:")
        for device_id, device_obj in connected_devices.items():
            print(f"{device_id}: {device_obj.get_sensors()}")
    else:
        print("No devices are connected.")

try:
    while True:
        command = input("Enter command pls: ")
        if command == "list_devices":
            list_devices()
        elif command == "verify":
            verify_all_devices()
        else:
            send_request(command)

        time.sleep(0.1)
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8', errors='ignore').strip()
            if message:
                print(f"Received message: {message}")

except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close()
    GPIO.cleanup()
