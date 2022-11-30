from datetime import datetime, timedelta
from random import randint
from typing import List

from models import Bus, BusStop, BusData

MAX_SEATED_PASSENGERS = 40

bus_1_stop_names = [
    "Terminal João Goulart - Plataforma 3 (Laranja)",
    "Praça Araribóia (2)",
    "Campus Gragoatá - Educação Física",
    "Campus Do Gragoatá",
    "Rua Passo Da Pátria, 28",
    "Rua Passo Da Pátria, 151-469",
    "Solar Do Jambeiro",
    "Faculdade De Direito",
    "Rua Presidente Pedreira, 312-406",
    "Praça Getúlio Vargas",
    "Avenida Jornalista Alberto Francisco Torres, 312-360",
    "Avenida Jornalista Alberto Francisco Torres 453",
    "Rua Joaquim Távora, 50",
    "Rua Joaquim Távora, 140",
    "Rua Joaquim Távora, 184",
    "Avenida Almirante Ary Parreiras, 220-290",
    "Avenida Almirante Ary Parreiras, 283",
    "Avenida Almirante Ary Parreiras, 422-424",
    "Avenida Almirante Ary Parreiras, 458",
    "Posto De Saúde Vital Brazil",
    "Avenida Almirante Ary Parreiras, 652",
    "Ponto Final - Canto Do Rio"
]


def generate_fake_data(bus_stops: List[BusStop], way=1):
    stop_ids = [bus_stop.id for bus_stop in bus_stops]

    if way == -1:
        stop_ids = sorted(stop_ids, reverse=True)

    bus_id = bus_stops[0].bus_id

    bus_data = []
    trip_start_datetime = datetime.now()
    minutes_elapsed = 0
    seated_passengers = 0
    standing_passengers = 0
    total_passengers = seated_passengers + standing_passengers
    for index, stop_id in enumerate(stop_ids):
        entering_number_of_passengers = randint(0, 20)
        leaving_number_of_passengers = randint(0, 10)

        if index < len(stop_ids) / 2:  # no passengers leave if the bus has not completed (at least) half the trip
            leaving_number_of_passengers = 0

        if index == len(stop_ids) - 1:  # if it's the end of the trip
            leaving_number_of_passengers = total_passengers

        total_passengers += entering_number_of_passengers - leaving_number_of_passengers
        if total_passengers < 0:
            total_passengers = 0

        if total_passengers > MAX_SEATED_PASSENGERS:
            seated_passengers = MAX_SEATED_PASSENGERS
            standing_passengers = total_passengers - seated_passengers
        else:
            seated_passengers = total_passengers
            standing_passengers = 0
        bus_data.append(
            BusData(
                bus_id=bus_id,
                bus_stop_id=stop_id,
                way=way,
                seated_passengers=seated_passengers,
                standing_passengers=standing_passengers,
                created_at=trip_start_datetime + timedelta(minutes=minutes_elapsed),
                updated_at=trip_start_datetime + timedelta(minutes=minutes_elapsed),
            )
        )

        minutes_elapsed += randint(2, 5)
    return bus_data


def generate_mocks(db):
    bus_1 = Bus(name="47")
    update_bus(db, bus_1)
    bus_stops = [
        BusStop(
            bus_id=bus_1.id,
            name=bus_stop_name,
        )
        for bus_stop_name in bus_1_stop_names
    ]
    bus_1.stops = bus_stops
    update_bus(db, bus_1)
    bus_data = generate_fake_data(bus_stops)
    for datum in bus_data:
        db.session.add(datum)
        db.session.commit()

    # bus_1.data = bus_data
    # update_bus(db, bus_1)


def update_bus(db, bus):
    db.session.add(bus)
    db.session.commit()

