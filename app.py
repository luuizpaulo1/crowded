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


@app.route("/api/bus/<int:bus_id>")
def get_bus(bus_id: int) :
    _bus = db.session.get(Bus, bus_id)
    return _bus.json


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
    max_capacity = 80
    total_quantity = bus_json["last_data_received"]["standing_passengers"] + bus_json["last_data_received"]["seated_passengers"]
    capacity_percent = int((total_quantity / max_capacity) * 100)
    return render_template("bus.html", bus=bus_json, capacity_percent=capacity_percent, max_capacity=max_capacity)


if __name__ == '__main__':
    app.run()
