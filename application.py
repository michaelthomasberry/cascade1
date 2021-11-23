from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///cascades.db")



#..... collect all data for output, layout, and hydraulic arrangement and controls
@app.route("/")
def index():
    return render_template("index.html")
    

#..... show BOM
@app.route("/bom", methods=["POST"])
def bom():
    bom_id = request.form.get("bom_id")
    bom = db.execute("SELECT * FROM bom WHERE bom_id = ?", bom_id)
    return render_template("bom.html",  bom = bom)

#..... display pack options...............................................................................................
@app.route("/search", methods=["POST"])
def search():
    #..... grab the data from the / route and save user inputs as variables
    output = request.form.get("output")
    hydraulic = request.form.get("hydraulic")
    layout = request.form.get("layout")
    controls = request.form.get("controls")
    #...... add a tolerence range for the output to give installer more options - the tolerence range should be agreed. 
    min_output = int(output) - 15
    max_output = int(output) + 15
    
    #..... show the casacade pack from cascades table in the database that matches the users perameters 
    cascades = db.execute("SELECT * FROM cascades WHERE hydraulic = ? AND layout =? AND output BETWEEN ? and ?", hydraulic, layout, min_output, max_output)
    #..... show the BOM of that pack
    rows = db.execute("SELECT * FROM bom JOIN cascades ON bom.bom_id = cascades.id WHERE output = ? AND hydraulic = ? AND layout =?", output, hydraulic, layout,)
    #..... TODO show control option + number of heating and hotwater circuits
    controls = db.execute("SELECT * FROM controls WHERE controls_description = ?", controls)
    return render_template("search.html",  cascades = cascades, rows = rows, controls = controls)
    
    #..... TODO implement a download pdf function that shows only the part numbers generated
    #..... Ensure mobile responsive on Heroku
    
    