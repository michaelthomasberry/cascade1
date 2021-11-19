from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///cascades.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    cascades = db.execute("SELECT * FROM cascades WHERE output= ?", request.form.get("pack") )
    rows = db.execute("SELECT * FROM bom JOIN cascades ON bom.bom_id = cascades.id WHERE output = ?", request.form.get("pack") )
    return render_template("search.html",  cascades = cascades, rows = rows)
