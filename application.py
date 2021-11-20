from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///cascades.db")



#..... collect all data for output, layout, and hydraulic arrangement
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    #..... grab the data from the form and save user inputs as variables
    output = request.form.get("output")
    hydraulic = request.form.get("hydraulic")
    layout = request.form.get("layout")
    controls = request.form.get("controls")
    #...... add a tolerence range for the output to give installer more options this should be set an agreed. 
    min_output = int(output) - 15
    max_output = int(output) + 15
    
    #..... show the casacade pack from cascades table in the database that matches the users perameters 
    cascades = db.execute("SELECT * FROM cascades WHERE hydraulic = ? AND layout =? AND output BETWEEN ? and ? ORDER BY price", hydraulic, layout, min_output, max_output)
    #..... show the BOM of that pack
    rows = db.execute("SELECT * FROM bom JOIN cascades ON bom.bom_id = cascades.id WHERE output = ? AND hydraulic = ? AND layout =?", output, hydraulic, layout,)
    controls = db.execute("SELECT * FROM controls WHERE controls_description = ?", controls)
    return render_template("search.html",  cascades = cascades, rows = rows, controls = controls)
    #..... TODO show control option + number of heating and hotwater circuits