import time
import RPi.GPIO as GPIO
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
try:
    from Tkinter import Tk, Label, Button, Frame, PhotoImage
except:
    from tkinter import Tk, Label, Button, Frame, PhotoImage

# Drink Map
# ----------------------
# Contains a mapping for each drink to its  1) Ingredients
#                                           2) Image
#                                           3) Method of serving (i.e. shaken, stirred, none)
'''
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
    }
}
'''
drinkMap = {
    "purple": {
        "ingredients": {
            "red1": {
                "amount": .5,
                "unit" : "oz"
            },
            "red2": {
                "amount": .5,
                "unit" : "oz"
            },
            "blue1": {
                "amount":.25,
                "unit": "oz"
            },
            "blue2": {
                "amount":.75,
                "unit": "oz"
            }
        },
        "serve":"shaken"
    },
    "orange": {
        "ingredients": {
            "red1": {
                "amount": 1,
                "unit" : "oz"
            },
            "yellow1": {
                "amount":.75,
                "unit": "oz"
            },
            "yellow2":{
                "amount": 2.25,
                "unit": "oz"
            }
        },
        "serve":"shaken"
    },
    "green": {
        "ingredients": {
            "yellow1": {
                "amount": 2,
                "unit" : "oz"
            },
            "blue1": {
                "amount": 1,
                "unit": "oz"
            }
        },
        "serve":"shaken"
    }
}

# Unit Map
# --------------------
# Map of units to time (in s) it takes to dispense 1 of that unit 
unitMap = {
    "oz": 17.75
}

# Ingredient Map
# --------------------
# Map of ingredients to GPIO pins (vials)
'''
ingredientMap = {
    "tequila": 5,
    "contreau": 9,
    "lime-juice": 11,
    "gin": 19,
    "soda water": 13,
    "simple syrup": 6,
}
'''
ingredientMap = {
    "red1": 6,
    "blue1": 13,
    "yellow1": 19,
    "red2": 9,
    "blue2": 11,
    "yellow2": 5,
}

# Rasp Pi GPIO ports connected to relay board for pumps
gpioList = [10, 9, 11, 5, 6, 13, 19, 26]
airPumpList = [26, 10]

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

def setUpPumps():
    GPIO.setmode(GPIO.BCM)

    for pin in gpioList:
        GPIO.setup(pin, GPIO.IN)
        
setUpPumps()

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

# Initialize Window and set background to black to reflect colo theme.
window = Tk()
window.configure(background = "black")

# Rename title of Window.
window.title("User Interface for colo")

# Set windowsize to fit best for pi touchscreen.
window.minsize(width=800, height=400)

# Create frames to organize/separate between logo and prompt and drink option buttons.
topFrame = Frame(window).pack()
bottomFrame = Frame(window).pack()

# Add colo Logo to Window Top Frame.
Logo = PhotoImage(file = "colo_Logo.png")
# Displaying colo Logo using a 'Label' by passing the 'picture' variable to 'image' parameter.
Label(topFrame, image = Logo, padx = 0, pady = 0, borderwidth = 0, highlightthickness = 0).pack()

# Add buttons for drink options. Upon clicking,
orangePhoto = PhotoImage(file = 'drinks/orange.png')
Button(bottomFrame, image = orangePhoto, text = "Orange", command = partial(makeDrink, "orange"), compound = "top").pack(padx = 60, side="left")
greenPhoto = PhotoImage(file = 'drinks/green.png')
Button(bottomFrame, image = greenPhoto, text = "Green", command = partial(makeDrink, "green"), compound = "top").pack(padx = 60, side="left")
purplePhoto = PhotoImage(file = 'drinks/purple.png')
Button(bottomFrame, image = purplePhoto, text = "Purple", command = partial(makeDrink, "purple"), compound = "top").pack(padx = 60, side="left")

window.mainloop()