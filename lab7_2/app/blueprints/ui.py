from flask import Blueprint, render_template

ui = Blueprint("ui", __name__)

@ui.route("/")
def index():
    return render_template("index.html")

@ui.route("/warsztat")
def practice():
    return render_template("practice.html")
