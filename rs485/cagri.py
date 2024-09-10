import minimalmodbus
import RPi.GPIO as GPIO
import time

RE_DE_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RE_DE_PIN, GPIO.OUT)

instrument = minimalmodbus.Instrument('/dev/ttyS0', 1)
instrument.serial.baudrate = 9600
instrument.serial.timeout = 2.0
instrument.debug = True

def set_re_de_pin(state):
    GPIO.output(RE_DE_PIN, state)
    time.sleep(0.1)

def read_dht11():
    try:
        set_re_de_pin(GPIO.HIGH)
        time.sleep(0.1)
        set_re_de_pin(GPIO.LOW)
        time.sleep(0.1)
        dht_value = instrument.read_register(0, 0)
        print(f"DHT11 temperature value from Arduino: {dht_value}°C")
    except Exception as e:
        print("An error occurred while reading DHT11: " + str(e))

if __name__ == '__main__':
    while True:
        read_dht11()
        time.sleep(5)
