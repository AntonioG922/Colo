# Colo Shaker
# Updated 4/3/19

from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.output(DIR, CW) #sets rotations CW

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

GPIO.output(MODE, RESOLUTION['Half'])

step_count = SPR * 2 #400 steps
delay = .005 #initial delay

for x in range(1,step_count):
    mod = x/100
    if mod>1:
        mod=1
    delay = 0.005/((mod+1)) # should start slow and ramp up speed
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)



GPIO.cleanup()
