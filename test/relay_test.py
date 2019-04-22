import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpioList = [26, 19, 13, 6, 5, 11, 9, 10]   
t = 5          #Sleep Time

for pin in gpioList:
    GPIO.setup(pin, GPIO.OUT)
    #GPIO.output(pin, GPIO.HIGH)

try:
    for pin in gpioList:
        print(pin)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(t)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(t)
        

except KeyboardInterrupt:
    print("Quitting...\n")

    # Reset GPIO settings

    GPIO.cleanup()

GPIO.cleanup()
