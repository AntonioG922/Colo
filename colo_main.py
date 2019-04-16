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

# P = pump
P1 = 10
P2 = 9
P3 = 11
P4 = 5
P5 = 6
P6 = 13
P7 = 19
P8 = 26

# Shaker (indicated by _s)
DIR_s = 23
STEP_s = 24
MODE_s = (14,15,18)
LSwitch_1_s = 6
##LSwitch_2_s = 7

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
GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_s, GPIO.OUT)
GPIO.setup(STEP_s, GPIO.OUT)
GPIO.setup(MODE_s, GPIO.OUT)
GPIO.setup(LSwitch_1_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(DIR_c, GPIO.OUT)
GPIO.setup(STEP_c, GPIO.OUT)
GPIO.setup(MODE_c, GPIO.OUT)
GPIO.setup(LSwitch_c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(MODE_s, RESOLUTION['Full']) # Shaker stepping
GPIO.output(MODE_c, RESOLUTION['Full']) # Conveyor stepping




#----------------------Resetting mechanical components----------------------

def reset_conveyor():
    
