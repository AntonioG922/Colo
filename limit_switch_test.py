#Limit Switch Test
#Created 4/11/19
#Updated 4/11/19

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #pin 15 is connected to the switch

while True: # Setup a while loop to wait for a button press
    if(GPIO.input(15)): # Setup an if loop to run a shutdown command when button press sensed
        print('1')
        break
    else:
        print('0')
    sleep(1)
