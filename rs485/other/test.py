import time
import serial
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
rs485 = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout=1
)
i = [1,4,6,12]

while True:
	GPIO.output(12,GPIO.LOW)
	time.sleep(0.01)
	if rs485.in_waiting > 0:
		data = rs485.read(1)
		temperature = int.from_bytes(data,byteorder='little',signed = False)
		print(f"Temperature: {temperature}°C")
	time.sleep(1)
