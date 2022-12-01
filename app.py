from datetime import datetime

from flask import Flask, render_template
from sqlalchemy.exc import IntegrityError

from db import db
from mocks import generate_mocks
from models import *  # noqa

app = Flask(__name__, template_folder="./templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db.init_app(app)

with app.app_context() as ctx:
    db.create_all()
    try:
        generate_mocks(db)
    except IntegrityError:
        pass


@app.route("/api")
def index():
    return {"server datetime": f"{datetime.now()}"}


@app.route("/api/buses")
def get_buses():
    buses_json = []
    for _bus in db.session.query(Bus):
        buses_json.append(_bus.json)
    return buses_json


@app.route("/")
def home():
    buses_json = []
    for _bus in db.session.query(Bus):
        buses_json.append(_bus.json)
    return render_template("index.html", buses=buses_json)


@app.route("/bus/<int:bus_id>")
def bus(bus_id):
    _bus = db.session.get(Bus, bus_id)
    bus_json = _bus.json
    return render_template("bus.html", bus=bus_json)

if __name__ == '__main__':
    app.run()
