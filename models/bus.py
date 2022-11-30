from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import relationship

from db import db


class BusData(db.Model):
    __tablename__ = "bus_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("bus.id"))
    bus_stop_id = Column(Integer, ForeignKey("bus_stop.id"))
    way = Column(Integer)  # 1 or -1
    seated_passengers = Column(Integer)
    standing_passengers = Column(Integer)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


class BusStop(db.Model):
    __tablename__ = "bus_stop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("bus.id"))
    name = Column(String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    data = relationship(BusData, backref="bus_stop")


class Bus(db.Model):
    __tablename__ = "bus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())
    stops = relationship(BusStop)
    data = relationship(BusData)

    @property
    def json(self):
        try:
            last_data_id = max([data.id for data in self.data])
            last_data_received = [data for data in self.data if data.id == last_data_id][0]
        except ValueError:
            last_data_received = None
        return {
            "id": self.id,
            "name": self.name,
            "stops": [
                {
                    "id": stop.id,
                    "name": stop.name,
                }
                for stop in self.stops
            ],
            "last_data_received": {
                "bus_stop_name": last_data_received.bus_stop.name,
                "bus_stop_id": last_data_received.bus_stop_id,
                "seated_passengers": last_data_received.seated_passengers,
                "standing_passengers": last_data_received.standing_passengers,
                "created_at": last_data_received.created_at
            } if last_data_received else None,
        }
