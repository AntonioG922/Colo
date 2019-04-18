# Colo Main
# Updated 4/15/19

from time import *
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

# Conveyor (indicated by _c)
DIR_c = 23
STEP_c = 24
MODE_c = (14,15,18)
LSwitch_c = 25


# Shake (_s)
DIR_s = 2
STEP_s = 3
MODE_s = (17,27,22)
LSwitch_s = 4

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
GPIO.setup(LSwitch_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

APS = 1.8 #angle per full step in degrees

#----------------------Resetting mechanical components----------------------

def reset_conveyor():
    conv_reset_steps = SPR*60 #doubled for half-step
    
    GPIO.output(MODE_c, RESOLUTION['Full']) #changes to half-step
    GPIO.output(DIR_c, CW)

    conv_res_delay = 0.005/8
    
    for x in range(conv_reset_steps):
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(conv_res_delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(conv_res_delay)
        if(GPIO.input(LSwitch_c)): 
            conv_dist = 0 #zeroes the conveyor distance
            return conv_dist
            break


def reset_shaker():

    shak_reset_steps = SPR*0.833*2 #doubled for half-step

    GPIO.output(MODE_s, RESOLUTION['Half']) #changes to half-step
    

    shak_res_delay = 0.01
    
    for x in range(shak_reset_steps): #find right bound
        GPIO.output(DIR_s, CW)
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(shak_res_delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(shak_res_delay)
        if(GPIO.input(LSwitch_s)): 
            shak_ang = 0 #zeroes the conveyor distance
            # limit switches should be set -120 and 120 degrees from top
            return shak_ang
            break

    sleep(1.5)
    

#------------------------------Drink Map-------------------------------
# Contains a mapping for each drink to its  1) Ingredients
#                                           2) Image
#                                           3) Method of serving (i.e. shaken, stirred, none)
drinkMap = {
    "Margarita": {
        "ingredients": {
            "tequila": {
                "amount": 2,
                "unit": "oz"
            },
            "contreau": {
                "amount": 1,
                "unit": "oz"
            },
            "lime-juice": {
                "amount": 1,
                "unit": "oz"
            }
        },
        "serve": "shaken"
    },
    "Ginn fizz": {
        "ingredients": {
            "gin": {
                "amount": 2,
                "unit": "oz"
            },
            "simple syrup": {
                "amount": 0.75,
                "unit": "oz"
            },
            "lime-juice": {
                "amount": 0.75,
                "unit": "oz"
            },
            "Soda Water":{
                "amount":1.5,
                "unit": "oz"
            }
        },
        "serve": "shaken"
    },
    "Gimlet": {
        "ingredients": {
            "gin": {
                "amount": 2,
                "unit": "oz"
            },
            "simple syrup": {
                "amount": 0.75,
                "unit": "oz"
            },
            "lime-juice": {
                "amount": 0.75,
                "unit": "oz"
            }
        },
        "serve": "shaken"
    },
    "Kamikaze": {
        "ingredients": {
            "vodka": {
                "amount": 1,
                "unit": "oz"
            },
            "triple-sec": {
                "amount": 1,
                "unit": "oz"
            },
            "lime-juice": {
                "amount": 1,
                "unit": "oz"
            }
        },
        "serve": "shaken"
    }
}

# Map of units to time (in s) it takes to dispense 1 of that unit 
unitMap = {
    "oz": 17.75
}

# Ingredient Map
# --------------------
# Map of ingredients to GPIO pins (vials)
# Map below needs to be updated
ingredientMap = {
    "tequila": 5,
    "contreau": 9,
    "lime-juice": 11,
    "gin": 19,
    "soda water": 13,
    "simple syrup": 6,
}


#---------------------------------Fill the Shaker----------------------------------

def makeDrink(drinkName):
    drink = drinkMap[drinkName]

    ingredientList = drink['ingredients']
    
    # Make the Pool of workers
    pool = ThreadPool(len(ingredientList))

    pool.map(lambda x: dispenseIngredient(x, drinkName), ingredientList)
    
    # Close the pool and wait for the work to finish 
    pool.close()
    pool.join()

    # Clean out any liquid left in pipes
    pumpAir()

def dispenseIngredient(ingredient, drinkName):
    pin = getPinFromIngredient(ingredient)
    activatePump(pin)
    time.sleep(getPumpTime(ingredient, drinkName))
    disablePump(pin)

def getPumpTime(ingredient, drinkName):
    unitTime = unitMap[drinkMap[drinkName]['ingredients'][ingredient]['unit']]
    return drinkMap[drinkName]['ingredients'][ingredient]['amount'] * unitTime

def activatePump(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    print('Activating pin ' + str(pin) + '...')

def disablePump(pin):
    GPIO.setup(pin, GPIO.IN)
    print('Disabling pin ' + str(pin) + '...')

def getPinFromIngredient(ingredient):
    return ingredientMap[ingredient]

def pumpAir():
    for pump in airPumpList:
        activatePump(pump)
    
    time.sleep(10)

    for pump in airPumpList:
        disablePump(pump)


#--------------------------------------Shake---------------------------------------
def shakeDrink():
    GPIO.output(MODE_s, RESOLUTION['Half']) # make sure everything else changes 
    
    shake_steps = round(200*0.3)*2 #120 steps: doubled because of half step

    
    # initial shake since it starts at the top
    GPIO.output(DIR_s, CW) #sets rotations CW
    for x in range(1,shake_steps):
        mod,rem = divmod(x,20) #every twenty steps increase speed
        if mod>3:
            mod=7-mod
            
        delay = 0.01/((mod+1)) # should start slow and ramp up speed
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(delay)
    
    sleep(0.5)

    shakes = 1
    
    while shakes<9: #shake 10 times
        GPIO.output(DIR_s, CCW) #sets rotations CW
        for x in range(1,shake_steps*2): #240 steps: goes from +108 to -108
            mod,rem = divmod(x,20)
            if mod>6:
                mod=13-mod
                
            delay = 0.01/((mod+1)) # should start slow and ramp up speed
            GPIO.output(STEP_s, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_s, GPIO.LOW)
            sleep(delay)

        sleep(0.5)

        GPIO.output(DIR_s, CW) #sets rotations CCW
        for x in range(1,shake_steps*2): #240 steps: goes from -108 to +108
            mod,rem = divmod(x,20)
            if mod>6:
                mod=13-mod
                
            delay = 0.01/((mod+1)) # should start slow and ramp up speed
            GPIO.output(STEP_s, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_s, GPIO.LOW)
            sleep(delay)

        shakes+=1

    GPIO.output(DIR_s, CCW) #sets rotations CW
    for x in range(1,shake_steps): #120 steps: goes from +108 to 0
        mod,rem = divmod(x,20)
        if mod>3:
            mod=7-mod
            
        delay = 0.01/((mod+1)) # should start slow and ramp up speed
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(delay)

#-------------------------------------Conveyor-------------------------------------        

def move_conveyor_shots():
    shot1_dist = 175 #mm: needs to be changed
    shot2_dist = 225 #mm
    shot3_dist = 275 #mm

    GPIO.output(MODE_c, RESOLUTION['Full'])
    
    GPIO.output(DIR_c, CCW)
    delay = 0.005
    
    for x in range(SPR*60): #fill first shot
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist>=shot1_dist:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(30)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break

    for x in range(SPR*30): #fill second cup
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist>=shot2_dist:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(60)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break

    for x in range(SPR*30): #fill third cup
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist>=shot3_dist:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(60)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break

    GPIO.output(DIR_c, CW)
    
    for x in range(SPR*80): #come back to 10 mm from start
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist<=10:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(60)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break
    
def move_conveyor_cups():
    cup1_dist = 180 #mm: needs to be changed
    cup2_dist = 250 #mm


    GPIO.output(MODE_c, RESOLUTION['Full'])
    
    GPIO.output(DIR_c, CCW)
    delay = 0.005
    
    for x in range(SPR*60): #fill first shot
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist>=cup1_dist:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(30)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break

    for x in range(SPR*30): #fill second cup
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist>=cup2_dist:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(30)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break



    GPIO.output(DIR_c, CW)
    
    for x in range(SPR*80): #come back to 10 mm from start
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
        if conv_dist<=10:
            #activatePump(number of final pump pin)
            #activatePump(number of final pump pin)
            sleep(30)
            #disablePump(number of final pump pin)
            #disablePump(number of final pump pin)
            break

#------------------------------------Clean-up----------------------------------
try:
    conv_dist = reset_conveyor()
    print(conv_dist)
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
