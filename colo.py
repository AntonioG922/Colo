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
        "img": "",
        "serve": "shaken"
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
ingredientMap = {
    "tequila": 5,
    "contreau": 9,
    "lime-juice": 11
}

# Rasp Pi GPIO ports connected to relay board for pumps
gpioList = [10, 9, 11, 5, 6, 13, 19, 26]
airPumpList = [26, 10]

def makeDrink(drinkName):
    drink = drinkMap[drinkName]

    # If drink doesn't exist, end
    if not drink:
        print("Drink not found")
        return

    ingredientList = drink['ingredients']
    
    # Make the Pool of workers
    pool = ThreadPool(len(ingredientList))

    pool.map(dispenseIngredient, ingredientList)
    
    # close the pool and wait for the work to finish 
    pool.close()
    pool.join()

    pumpAir()

def setUpPumps():
    GPIO.setmode(GPIO.BCM)

    for pin in gpioList:
        GPIO.setup(pin, GPIO.IN)
        
setUpPumps()

def dispenseIngredient(ingredient):
    pin = getPinFromIngredient(ingredient)
    activatePump(pin)
    time.sleep(getPumpTime(ingredient))
    disablePump(pin)

def getPumpTime(ingredient):
    unitTime = unitMap[drinkMap['Margarita']['ingredients'][ingredient]['unit']]
    return drinkMap['Margarita']['ingredients'][ingredient]['amount'] * unitTime

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
    
    time.sleep(5)

    for pump in airPumpList:
        disablePump(pump)

#def addDrink(drinkName):

# Initialize Window and set background to black to reflect colo theme.
window = Tk()
window.configure(background = "black")

# Rename title of Window.
window.title("User Interface for colo")

# Set windowsize to fit best for pi touchscreen.
window.minsize(width=800, height=480)
window.maxsize(width=800, height=480)

# Create frames to organize/separate between logo and prompt and drink option buttons.
topFrame = Frame(window).pack()
bottomFrame = Frame(window).pack(side="bottom")

# Add colo Logo to Window Top Frame.
Logo = PhotoImage(file = "colo_Logo.png")
# Displaying colo Logo using a 'Label' by passing the 'picture' variable to 'image' parameter.
Label(topFrame, image = Logo, padx = 0, pady = 0, borderwidth = 0, highlightthickness = 0).pack()

# Add buttons for drink options. Upon clicking,
for drink in drinkMap:
    photo = PhotoImage(file = 'drinks/' + drink.lower() + '.png')
    Button(bottomFrame, text = drink, image = photo, command = partial(makeDrink, drink), compound = "top").pack(pady = 5)

window.mainloop()