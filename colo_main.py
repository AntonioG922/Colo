# Colo Main
# Updated 4/15/19

import time
import RPi.GPIO as GPIO
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

try:
    from Tkinter import Tk, Label, Button, Frame, PhotoImage
except:
    from tkinter import Tk, Label, Button, Frame, PhotoImage

#---------------------------------GPIO Setup ------------------------------

GPIO.setmode(GPIO.BCM)

# P = pump

gpioList = [10,9,11,5,6,13,19,26]

def setUpPumps():
    for pin in gpioList:
        GPIO.setup(pin, GPIO.IN)

setUpPumps()

# Shaker (indicated by _s)
DIR_s = 23
STEP_s = 24
MODE_s = (14,15,18)
LSwitch_left_s = 6
LSwitch_right_s = 7

# Conveyor
DIR_c = 2
STEP_c = 3
MODE_c = (17,27,22)
LSwitch_c = 4

# Modes
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

# Setup

GPIO.setup(DIR_s, GPIO.OUT)
GPIO.setup(STEP_s, GPIO.OUT)
GPIO.setup(MODE_s, GPIO.OUT)
GPIO.setup(LSwitch_1_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(DIR_c, GPIO.OUT)
GPIO.setup(STEP_c, GPIO.OUT)
GPIO.setup(MODE_c, GPIO.OUT)
GPIO.setup(LSwitch_c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(MODE_s, RESOLUTION['Half']) # Shaker stepping
GPIO.output(MODE_c, RESOLUTION['Half']) # Conveyor stepping

# Motor Spin Prelims

CW = 1
CCW = 0

SPR = 200 #200 full steps per revolution

DPS = 5/200 #distance per step: 5mm per full rotation

APS = 1.8 #angle per step in degrees

#----------------------Resetting mechanical components----------------------

def reset_conveyor():
    conv_reset_steps = SPR*60*2 #doubled for half-step
    
    GPIO.output(MODE_c, RESOLUTION['Half']) #changes to half-step
    GPIO.output(DIR_c, CW)

    conv_res_delay = 0.005/5
    
    for x in range(conv_reset_steps):
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(conv_res_delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(conv_res_delay)
        if(GPIO.input(LSwitch_c)): 
            conv_dist = 0 #zeroes the conveyor distance
            break

def reset_shaker():
    shak_reset_steps = SPR*0.833*2 #doubled for half-step

    GPIO.output(MODE_s, RESOLUTION['Half']) #changes to half-step
    

    shak_res_delay = 0.005
    
    for x in range(shak_reset_steps): #find right bound
        GPIO.output(DIR_s, CW)
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(shak_res_delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(shak_res_delay)
        if(GPIO.input(LSwitch_right_s)): 
            shak_ang = 120 #zeroes the conveyor distance
            break

    sleep(1.5)
    
    steps_to_top = round(0.333*200)*2 #120 degrees to the top times two for half step
    for x in range(shak_reset_steps): #come to top center
        GPIO.output(DIR_s, CCW)
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(shak_res_delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(shak_res_delay)
        shak_ang-= APS*0.5 #halfed for half step
        if shak_ang<=0:
            shak_ang = 0
            break

#---------------------------------Fill the Shaker----------------------------------

## Antonio should populate this section with everything in the prototype 1 thing

#--------------------------------------Shake---------------------------------------

           
#---------------------------------Clean-up----------------------------------
GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
