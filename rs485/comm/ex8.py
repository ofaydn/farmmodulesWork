import serial
import RPi.GPIO as GPIO
import time

# RS485 Direction Control Pin (connected to DE/RE pin of the RS485 module)
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

def send_request():
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch to transmit mode
    time.sleep(0.05)  # Delay to stabilize mode switch

    ser.write(b'S2_A\n')  # Send the request
    print("Request sent: 'S2_A'")

    time.sleep(0.05)  # Delay to ensure the data is sent
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Switch back to listening mode

def receive_response():
    timeout = time.time() + 2  # 2 seconds timeout
    response = ''

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data.isprintable():  # Check if data is printable
                response = data
                break
        if time.time() > timeout:
            print("Response timeout.")
            break

    return response

def main():
    while True:
        send_request()  # Constantly send the request
        response = receive_response()  # Wait for and process the response

        if response:
            current_time = time.strftime('%H:%M:%S')
            print(f"{current_time} - Received: {response}")
        else:
            print("No valid response received.")
        
        time.sleep(1)  # Wait before sending the next request

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()
        GPIO.cleanup()
        print("\nProgram terminated by user.")
