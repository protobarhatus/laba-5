import RPi.GPIO as GPIO
import time as time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17


GPIO.setmode(GPIO.BCM)

GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)


def toBin(n):
    return [int(i) for i in bin(n)[2:].zfill(8)]

def toVoltage(i):
    return 3.3 * i / 256

def setNum(n):
    for i in range(0, 8):
        GPIO.output(dac[i], toBin(n)[i])

def acp():
    for i in range(0, 256):
        setNum(i)
        time.sleep(0.0007)
        if (GPIO.input(comp) == 0):
            return i

try:
    while (True):
        print('Voltage = ', toVoltage(acp()), 'V')

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)