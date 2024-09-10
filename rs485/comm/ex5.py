import serial
import RPi.GPIO as GPIO
from datetime import datetime
import time

RS485_DE_RE_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Listening

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
    exit(1)

def send_request(slave_id):
    command = f'S{slave_id}_A\n'  # Create the command string based on the slave ID
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.01)  # Small delay to ensure mode switch
    ser.write(command.encode('utf-8'))  # Send the command
    print(f"Request sent: '{command.strip()}'")
    time.sleep(0.01)  # Small delay after sending
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to receive mode

def receive_response():
    timeout = time.time() + 2  # 2-second timeout
    response = ''
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    response = data
                    break
            except UnicodeDecodeError:
                print("Received non-UTF-8 data, skipping...")
                continue
        if time.time() > timeout:
            print("Response timeout.")
            break
    return response

def main():
    print("Welcome!")
    while True:
        print("\nWhat would you like to do?")
        print("1: Request Temperature")
        print("2: Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                slave_id = input("Which Slave? (1, 2): ")
                if slave_id.isdigit() and int(slave_id) > 0:
                    send_request(slave_id)
                    response = receive_response()
                    if response:
                        current_time = datetime.now().strftime('%H:%M:%S')
                        print(f"{current_time} - Temperature: {response}°C")
                    else:
                        print("No valid response received.")
                    break
                else:
                    print("Invalid input. Please enter a valid slave number (e.g., 1, 2).")
        elif choice == '2':
            print("Exiting.")
            ser.close()
            GPIO.cleanup()
            exit(0)
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()
        GPIO.cleanup()
        print("\nProgram terminated by user.")
