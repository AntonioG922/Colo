import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpioList = [9, 26]   
t = 30          #Sleep Time

GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)

for pin in gpioList:
    GPIO.setup(pin, GPIO.OUT)
    #GPIO.output(pin, GPIO.HIGH)

try:
    for pin in gpioList:
        print(pin)
        GPIO.output(pin, GPIO.LOW)

    time.sleep(t)
        
    for pin in gpioList:
        GPIO.output(pin, GPIO.HIGH)

        

except KeyboardInterrupt:
    print("Quitting...\n")

    # Reset GPIO settings

    GPIO.cleanup()

GPIO.cleanup()
