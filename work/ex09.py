import serial
import RPi.GPIO as GPIO
import time

# RS485 Direction Control Pin
RS485_DE_RE_PIN = 4

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in listening mode

# Setup serial connection
try:
    ser = serial.Serial(
        port='/dev/serial0',  # Use the correct serial port
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
    command = f'S{slave_id}_A\n'  # Create the command string
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(command.encode('utf-8'))  # Send the command as bytes
    print(f"Request sent: '{command.strip()}'")
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

def receive_response():
    timeout = time.time() + 2  # 2-second timeout
    response = ''
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data.isprintable():
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
            slave_id = input("Which Slave? (1, 2): ")
            if slave_id in ['1', '2']:
                send_request(slave_id)
                response = receive_response()
                if response:
                    print(f"Received response: {response}")
                else:
                    print("No valid response received.")
            else:
                print("Invalid input. Please enter a valid slave number (1 or 2).")
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