from flask import Flask
from flask import render_template
from time import *
import RPi.GPIO as GPIO
from multiprocessing.dummy import Pool as ThreadPool


#---------------------------------Site Setup ------------------------------
app = Flask(__name__)

@app.route('/')
def load_site():
    return render_template('index.html')

@app.route('/api/makeDrink/<drink>/<strength>')
def make_drink(drink, strength):
    try:
        makeDrink(drink)
        return
    except KeyboardInterrupt:
        GPIO.cleanup()

# Chaining the vials on the url is not the best way
# to do this but its easy and YOLO for COLO
@app.route('/api/updateVials/<vial1>/<vial2>/<vial3>/<vial4>/<vial5>/<vial6>')
def update_vials(vial1, vial2, vial3, vial4, vial5, vial6):
    ingredientMap = {}
    ingredientMap[vial1] = 5
    ingredientMap[vial2] = 9
    ingredientMap[vial3] = 11
    ingredientMap[vial4] = 19
    ingredientMap[vial5] = 13
    ingredientMap[vial6] = 6
    
    return

# See above chaining comment
@app.route('/api/addDrink/<name>/<served>/<ingrdnt1>/<ingrdnt1Amount>/<ingrdnt1Unit>/<ingrdnt2>/<ingrdnt2Amount>/<ingrdnt2Unit>')
@app.route('/api/addDrink/<name>/<served>/<ingrdnt1>/<ingrdnt1Amount>/<ingrdnt1Unit>/<ingrdnt2>/<ingrdnt2Amount>/<ingrdnt2Unit>/<ingrdnt3>/<ingrdnt3Amount>/<ingrdnt3Unit>')
def add_drink(name, served, ingrdnt1, ingrdnt1Amount, ingrdnt1Unit, ingrdnt2, ingrdnt2Amount, ingrdnt2Unit, ingrdnt3 = None, ingrdnt3Amount = None, ingrdnt3Unit = None):
    ingredients = {}
    ingredients[ingrdnt1] = {
        'amount': ingrdnt1Amount,
        'unit': ingrdnt1Unit
    }
    ingredients[ingrdnt2] = {
        'amount': ingrdnt2Amount,
        'unit': ingrdnt2Unit
    }
    if(ingrdnt3):
        ingredients[ingrdnt3] = {
            'amount': ingrdnt3Amount,
            'unit': ingrdnt3Unit
        }
    
    
    drinkMap[name] = {
        'ingredients': ingredients,
        'served': served
    }
    
    return

#---------------------------------GPIO Setup ------------------------------

GPIO.setmode(GPIO.BCM)

gpioList = [10,9,11,5,6,13,19,26]

final_pump1 = 9
final_pump2 = 10

def setUpPumps():
    for pin in gpioList:
        GPIO.setup(pin, GPIO.IN)

setUpPumps()

# Conveyor (indicated by _c)
DIR_c = 23
STEP_c = 24
MODE_c = (18,15,14)
LSwitch_c = 25


# Shake (_s)
DIR_s = 2
STEP_s = 3
MODE_s = (22,27,17)
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

conv_dist = 0

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
        if limit_switch_hit(LSwitch_c): 
            conv_dist = 0 #zeroes the conveyor distance
            return


def reset_shaker():
    GPIO.output(MODE_s, RESOLUTION['Half']) #changes to half-step

    #assuming it shouldn't be more than a qtr turn from 0
    hit_limit_switch = spin_shaker(CCW, 0.25)
    sleep(1.5)
    if not hit_limit_switch:
        spin_shaker(CW, 0.5)
        sleep(1.5)
    
def spin_shaker(direction, num_turns):
    shak_reset_steps = SPR*2 #doubled for half-step
    shak_res_delay = 0.005
    for x in range(int(round(shak_reset_steps*num_turns))): 
        GPIO.output(DIR_s, direction)
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(shak_res_delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(shak_res_delay)
        if limit_switch_hit(LSwitch_s): 
            return True
    return False
    
def limit_switch_hit(l_switch):
    return GPIO.input(l_switch)

#------------------------------Drink Map-------------------------------
# Contains a mapping for each drink to its  1) Ingredients
#                                           2) Image 
#                                           3) Method of serving (i.e. shots, cocktail)


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
        "serve": "shot"
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
        "serve": "cocktail"
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
        "serve": "shot"
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
        "serve": "shot"
    },
    "Lemon Drop Shot": {
        "ingredients": {
            "lemon-juice": {
                "amount": 1.5,
                "unit": "oz"
            },
            "vodka": {
                "amount": 1.5,
                "unit": "oz"
            },
            "simple-syrup": {
                "amount": 1.5,
                "unit": "oz"
            }
        },
        "serve": "shot"
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
    "simple-syrup": 19,
    "vodka": 11,
    "lemon-juice": 13,
    "gin": 6,
    "soda water": 5,
}

#-------------------------------Make Drink Function----------------------------------

def makeDrink(drinkName):
    # Reset shit
    reset_conveyor()
    reset_shaker()
    
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

    # Shake the Drink
    shakeDrink()

    # Conveyor movement
    shot_or_cup = drink['serve']
    if shot_or_cup=='shot':
        move_conveyor_shots()
    else:
        move_conveyor_cocktail()
    

#---------------------------------Fill the Shaker----------------------------------

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
    activatePump(26)
    
    time.sleep(20)

    disablePump(26)


#--------------------------------------Shake---------------------------------------
def shakeDrink():
    GPIO.output(MODE_s, RESOLUTION['Half']) # make sure everything else changes 
    
    shake_steps = round(200*0.41)*2 #164 half steps: doubled because of half step
    
    # initial shake since it starts at the top
    GPIO.output(DIR_s, CW) #sets rotations CW
    for x in range(1,int(shake_steps)):
        mod,rem = divmod(x,20) #every twenty steps increase speed
        if mod>8:
            mod=9-mod
            
        delay = 0.01/((mod+1)) # should start slow and ramp up speed
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(delay)
    

    shakes = 1
    
    while shakes<9: #shake 10 times counting first and last moves
        GPIO.output(DIR_s, CCW) #sets rotations CW
        for x in range(1,int(shake_steps*2)): #328 steps: goes from +108 to -108
            mod,rem = divmod(x,20)
            if mod>8:
                mod=17-mod
                
            delay = 0.01/((mod+1)) # should start slow and ramp up speed
            GPIO.output(STEP_s, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_s, GPIO.LOW)
            sleep(delay)

        GPIO.output(DIR_s, CW) #sets rotations CCW
        for x in range(1,int(shake_steps*2)): #328 steps: goes from -108 to +108
            mod,rem = divmod(x,20)
            if mod>8:
                mod=17-mod
                
            delay = 0.01/((mod+1)) # should start slow and ramp up speed
            GPIO.output(STEP_s, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP_s, GPIO.LOW)
            sleep(delay)

        shakes+=1

    sleep(0.5)
    
    GPIO.output(DIR_s, CCW) #sets rotations CW
    for x in range(1,int(shake_steps*2)): #328 steps: goes slower until it hits the zero switch
        mod,rem = divmod(x,40)
        if mod>4:
            mod=9-mod
            
        delay = 0.01/((mod+1)) # should start slow and ramp up speed
        GPIO.output(STEP_s, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_s, GPIO.LOW)
        sleep(delay)
        if(GPIO.input(LSwitch_s)): 
            shak_ang = 0 #zeroes the conveyor distance
            return shak_ang
            break
    
#-------------------------------------Conveyor-------------------------------------        

def move_conveyor_shots():
    shot1_dist = 101.6 #mm: needs to be changed
    shot2_dist = 152 #mm
    shot3_dist = 203 #mm

    GPIO.output(MODE_c, RESOLUTION['Full'])
    
    GPIO.output(DIR_c, CCW)
    delay = 0.005

    disp_delay = 17.75*1.5/2 #how long to run a shot
    first_disp = disp_delay + 10
    last_disp = disp_delay + 10
    
    move_conveyor(shot1_dist)
    pump_into_cup(first_disp)

    move_conveyor(shot2_dist)
    pump_into_cup(disp_delay)

    move_conveyor(shot3_dist)
    pump_into_cup(last_disp)

    GPIO.output(DIR_c, CW)
    
    reset_conveyor()
    
def move_conveyor_cocktail():
    cup1_dist = 180 #mm: needs to be changed
    cup2_dist = 250 #mm

    GPIO.output(MODE_c, RESOLUTION['Full'])
    
    GPIO.output(DIR_c, CCW)

    disp_delay = 17.75*1.5
    
    move_conveyor(cup1_dist)
    pump_into_cup(disp_delay)

    move_conveyor(cup2_dist)
    pump_into_cup(disp_delay)

    GPIO.output(DIR_c, CW)

    reset_conveyor()

def move_conveyor(final_pos):
    delay = 0.005
    while conv_dist < final_pos:
        GPIO.output(STEP_c, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_c, GPIO.LOW)
        sleep(delay)
        conv_dist+=DPS
    return


def pump_into_cup(disp_delay):
    activatePump(final_pump1)
    activatePump(final_pump2)
    sleep(disp_delay)
    disablePump(final_pump1)
    disablePump(final_pump2)
    return

try:
    makeDrink("Lemon Drop Shot")
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()