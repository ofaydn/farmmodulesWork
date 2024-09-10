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
        baudrate=19200,
        timeout=1
    )
except serial.SerialException as e:
    print(f"Failed to connect to serial port: {e}")
    raise

def send_request(slave_id):
    # Example: Sending a request to the slave
    GPIO.output(4, GPIO.HIGH)  # Set GPIO4 to HIGH for sending data
    request = f"S{slave_id}_A\n"
    ser.write(request.encode('utf-8'))
    GPIO.output(4, GPIO.LOW)  # Set GPIO4 to LOW after sending data
    time.sleep(0.01)  # Small delay to ensure the line is stable

def receive_response():
    try:
        GPIO.output(4, GPIO.LOW)  # Set GPIO4 to LOW for receiving data
        time.sleep(0.01)  # Small delay to ensure the line is stable

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            GPIO.output(4, GPIO.HIGH)  # Set GPIO4 to HIGH after reading
            if data:
                return data
            else:
                raise ValueError("Received empty data from slave")
    except ValueError as ve:
        print(f"Data error: {ve}")
    except serial.SerialTimeoutException:
        print("Timeout: No data received from slave")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        GPIO.output(4, GPIO.HIGH)  # Ensure GPIO4 is HIGH for idle state
    return None

def main():
    print("Welcome!")
    print("What would you like to do?")
    print("1: Send data")
    print("2: Receive data")
    choice = input("Enter your choice: ")

    slave_id = input("Enter the slave ID (e.g., 1): ")

    if choice == '1':
        data = input("Enter the data to send: ")
        send_request(slave_id)
        print(f"Sent data to slave {slave_id}")
    elif choice == '2':
        send_request(slave_id, 'REQUEST_TEMP')
        response = receive_response()
        if response is not None:
            print(f"Received response from slave {slave_id}: {response}°C")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
