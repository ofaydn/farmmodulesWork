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
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
except serial.SerialException as e:
    print(f"Failed to connect to serial port: {e}")
    raise

def send_request():
    GPIO.output(4, GPIO.HIGH)  # Set GPIO4 to HIGH for sending data
    time.sleep(0.1)
    ser.write(b'Z')  # Send request to slave
    print("Sent request!")
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
    while True:
       print("What would you like to do?")
       print("1: Send request for temperature")
       print("2: Exit")
       choice = input("Enter your choice: ")

       if choice == '1':
           send_request()
           response = receive_response()
           if response is not None:
               current_time = datetime.now().strftime('%H:%M:%S')
               print(f"{current_time} - Temperature: {response}°C")
           else:
               print("No response received.")
       elif choice == '2':
           print("Exiting.")
           exit(1)
       else:
           print("Invalid choice")

if __name__ == "__main__":
    main()
