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
    return 'Vials updated: ' + vial1

# See above chaining comment
@app.route('/api/addDrink/<name>/<ingrdnt1>/<ingrdnt1Amount>/<ingrdnt1Unit>/<ingrdnt2>/<ingrdnt2Amount>/<ingrdnt2Unit>/<ingrdnt3>/<ingrdnt3Amount>/<ingrdnt3Unit>/<served>')
def add_drink(name, ingrdnt1, ingrdnt1Amount, ingrdnt1Unit, ingrdnt2, ingrdnt2Amount, ingrdnt2Unit, ingrdnt3, ingrdnt3Amount, ingrdnt3Unit, served):
    return 'Drink Added: ' + name + ingrdnt1 + served
