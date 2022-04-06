import RPi.GPIO as GPIO
import time as time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17


GPIO.setmode(GPIO.BCM)

GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)
GPIO.setup (leds, GPIO.OUT)


def toBin(n):
    return [int(i) for i in bin(n)[2:].zfill(8)]

def toVoltage(i):
    return 3.3 * i / 256

def setNum(n):
    for i in range(0, 8):
        GPIO.output(dac[i], toBin(n)[i])

def setLeds(n):
    for i in range(0, 8):
        GPIO.output(leds[i], toBin(n)[i])


def checkComp(m):
    setNum(m)
    time.sleep(0.001)
    return 1 - GPIO.input(comp)

def acp():
    left = 0
    r = 255
    while (r - left > 1):
        m = int((r + left) / 2)
        if (checkComp(m) == 0):
            left = m
        else:
            r = m

    
    return left

try:
    while (True):
        v = acp()
        print('Voltage = ', toVoltage(v), 'V')
        setLeds(v - v % 4)


finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.output(leds, 0)