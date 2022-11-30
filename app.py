from datetime import datetime

from flask import Flask
from sqlalchemy.exc import IntegrityError

from db import db
from mocks import generate_mocks
from models import *  # noqa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db.init_app(app)

with app.app_context() as ctx:
    db.create_all()
    try:
        generate_mocks(db)
    except IntegrityError:
        pass


@app.route("/")
def index():
    return {"server datetime": f"{datetime.now()}"}


@app.route("/buses")
def get_buses():
    buses_json = []
    for _bus in db.session.query(Bus):
        buses_json.append(_bus.json)
    return buses_json


if __name__ == '__main__':
    app.run()
