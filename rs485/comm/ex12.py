import serial
import RPi.GPIO as GPIO
import time

# RS485 Direction Control Pin
RS485_DE_RE_PIN = 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in listening mode

# Setup serial connection
try:
    ser = serial.Serial(
        port='/dev/ttyS0',  # Use the correct serial port
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except serial.SerialException as e:
    print(f"Failed to connect to serial port: {e}")
    exit(1)

def send_request(command):
    full_command = f'{command}\n'  # Create the full command string
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)
    ser.write(full_command.encode('utf-8'))  # Send the command as bytes
    print(f"Request sent: '{full_command.strip()}'")
    time.sleep(0.05)
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

def receive_response():
    responses = []  # Collect all responses
    timeout = time.time() + 2  # 2-second window to collect responses
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data.isprintable():
                    responses.append(data)
            except UnicodeDecodeError:
                print("Received non-UTF-8 data, skipping...")
                continue
        if time.time() > timeout:
            break
    return responses

def main():
    print("Welcome!")
    while True:
        command = input("Enter command to send (or type 'exit' to quit): ")

        if command.lower() == 'exit':
            print("Exiting.")
            ser.close()
            GPIO.cleanup()
            exit(0)

        send_request(command)
        responses = receive_response()
        if responses:
            for response in responses:
                print(f"Received response: {response}")
        else:
            print("No valid response received.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()
        GPIO.cleanup()
        print("\nProgram terminated by user.")
