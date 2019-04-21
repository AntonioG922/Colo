import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpioList = [26, 19, 13, 6, 5, 11, 9, 10]   
t = 4          #Sleep Time

for pin in gpioList:
    GPIO.setup(pin, GPIO.OUT)
    #GPIO.output(pin, GPIO.HIGH)

try:
    while True:
        GPIO.output(19, GPIO.LOW)
        time.sleep(t)
        GPIO.output(19, GPIO.HIGH)
        time.sleep(t)

except KeyboardInterrupt:
    print("Quitting...\n")

    # Reset GPIO settings

    GPIO.cleanup()