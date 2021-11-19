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
    pack = request.form.get("pack")
    hydraulic = request.form.get("hydraulic")
    layout = request.form.get("layout")
    #..... show the casacade pack from cascades table in the database that matches the users perameters 
    cascades = db.execute("SELECT * FROM cascades WHERE output= ? AND hydraulic = ? AND layout =?", pack, hydraulic, layout,)
    #..... show the BOM of that pack
    rows = db.execute("SELECT * FROM bom JOIN cascades ON bom.bom_id = cascades.id WHERE output = ? AND hydraulic = ? AND layout =?", pack, hydraulic, layout,)
    return render_template("search.html",  cascades = cascades, rows = rows)
