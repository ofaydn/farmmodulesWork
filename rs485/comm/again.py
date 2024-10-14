import time
import serial
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)

send = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

i = [0,10,45,90,135,180,135,90,45,10,0]
try:
    while True:
     for x in i:
         GPIO.output(17, GPIO.HIGH)
         send.write(str(x).encode('utf-8'))
         GPIO.output(17, GPIO.LOW)
         print(x)
         time.sleep(1.5)
except KeyboardInterrupt:
    # Close the serial port and clean up GPIO settings
    send.close()
    GPIO.cleanup()
