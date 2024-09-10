import serial
import RPi.GPIO as GPIO
from datetime import datetime
import time

# RS485 DE/RE Pin Tanımı
RS485_DE_RE_PIN = 4

# GPIO Ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Başlangıçta dinleme modunda

# Seri Port Ayarları
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

def send_request():
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Gönderme moduna geç
    time.sleep(0.01)  # Mod değişimi için kısa bir gecikme
    ser.write(b'S1_A\n')
    print("Request sent: 'S1_A'")
    time.sleep(0.01)  # Veri gönderimi sonrası kısa bir gecikme
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Dinleme moduna geç

def receive_response():
    timeout = time.time() + 2  # 2 saniyelik timeout
    response = ''
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data:
                response = data
                break
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
            send_request()
            response = receive_response()
            if response:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"{current_time} - Temperature: {response}°C")
            else:
                print("No valid response received.")
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
