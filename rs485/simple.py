import serial
from datetime import datetime

# Open the serial port with appropriate settings
ser = serial.Serial(
    port='/dev/serial0',  # This is the primary UART (TXD0/RXD0 on GPIO14/15)
    baudrate=9600,
    timeout=1
)

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"{current_time} - Temperature: {data}°C")
