from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def load_site():
    return render_template('index.html')

@app.route('/api/makeDrink/<drink>/<strength>')
def make_drink(drink, strength):
    return 'Drink Made' + drink + strength

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

    return 'Vials updated: ' + vial1 + ': ' + ingredientMap[vial1]

# See above chaining comment
@app.route('/api/addDrink/<name>/<ingrdnt1>/<ingrdnt1Amount>/<ingrdnt1Unit>/<ingrdnt2>/<ingrdnt2Amount>/<ingrdnt2Unit>/<ingrdnt3>/<ingrdnt3Amount>/<ingrdnt3Unit>/<served>')
def add_drink(name, ingrdnt1, ingrdnt1Amount, ingrdnt1Unit, ingrdnt2, ingrdnt2Amount, ingrdnt2Unit, ingrdnt3, ingrdnt3Amount, ingrdnt3Unit, served):
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
    
    return 'Drink Added: ' + name + ingrdnt1 + served


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