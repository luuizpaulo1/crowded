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

bus_2_stop_names = [
    "Rua Doze Centro Niterói - Rio De Janeiro 24030 Brasil",
    "Centro Niterói - Rj 24030-250 Brasil",
    "Rua Professor Ernani Pires De Mello 58 São Domingos Niterói - Rj 24210-130 Brasil",
    "R. Visc. De Morais 176-214 - Ingá Niterói - Rj 24210-145 Brasil",
    "Rua Visconde De Morais 490",
    "R. Pres. Pedreira 142-156 - Ingá Niterói - Rj 24210-470 Brasil",
    "R. Dr. Paulo Alves 269-365 - Ingá Niterói - Rj 24210-445 Brasil",
    "Rua Álvares De Azevedo 2 Icaraí Niterói - Rj 24220-301 Brasil",
    "Avenida Jornalista Alberto Francisco Torres 329 Icaraí Niterói - Rj 24220-301 Brasil",
    "Avenida Jornalista Alberto Francisco Torres 453",
    "Rua Joaquim Távora, 50",
    "Rua Joaquim Távora 138 Icaraí Niterói - Rj 24220-301 Brasil",
    "Rua Joaquim Távora 181 Icaraí Niterói - Rj 24220-301 Brasil",
    "Rua Joaquim Távora Próximo Ao 800-866 - Icaraí Niterói - Rj 24230-540 Brasil",
    "Avenida Quintino Bocaiúva 127",
    "Avenida Quintino Bocaiúva 127",
    "Av. Quintino Bocaiúva 70-168 - São Francisco Niterói - Rj Brasil",
    "Avenida Quintino Bocaiúva 976 São Francisco Niterói - Rj 24370-001 Brasil",
    "Avenida Prefeito Silvio Picanço Próximo Ao 585-595 - Charitas Niterói - Rj 24360-030 Brasil",
    "Avenida Prefeito Sílvio Picanço Charitas Niterói - Rj 24370-001 Brasil",
    "Avenida Prefeito Silvio Picanço 449",
    "Avenida Prefeito Silvio Picanço Próximo Ao 1646-1746 - Charitas Niterói - Rj 24370-135 Brasil",
    "Charitas Niterói - Rj 24370-195 Brasil",
    "Avenida Carlos Ermelindo Marins Jurujuba Niterói - Rj 24370-195 Brasil",
    "Praia De Jurujuba 82 - Jurujuba Niterói - Rj 24370-197 Brasil",
    "Praia De Jurujuba 87 - Jurujuba Niterói - Rj 24370-197 Brasil",
    "Avenida Carlos Ermelindo Marins 15 Jurujuba Niterói - Rj 24370-195 Brasil",
    "Avenida Carlos Ermelindo Marins 136 Jurujuba Niterói - Rj 24370-195 Brasil",
    "Rua Lauro Sodré 34 - Jurujuba Niterói - Rj 24370-300 Brasil",
    "Av. Carlos Ermelindo Marins 2193-2437 - Jurujuba Niterói - Rj Brasil",
    "Travessa Beco Do Cahfaris Jurujuba Niterói - Rio De Janeiro Brasil",
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
    bus_1 = Bus(name="47 - Centro x Canto do Rio")
    update_bus(db, bus_1)
    bus_1_stops = [
        BusStop(
            bus_id=bus_1.id,
            name=bus_stop_name,
        )
        for bus_stop_name in bus_1_stop_names
    ]
    bus_1.stops = bus_1_stops
    update_bus(db, bus_1)
    bus_1_data = generate_fake_data(bus_1_stops)
    add_fake_data(db, bus_1_data)

    bus_2 = Bus(name="33 - Centro x Jurujuba")
    update_bus(db, bus_2)
    bus_2_stops = [
        BusStop(
            bus_id=bus_2.id,
            name=bus_stop_name,
        )
        for bus_stop_name in bus_2_stop_names
    ]
    bus_2.stops = bus_2_stops
    update_bus(db, bus_2)
    bus_2_data = generate_fake_data(bus_2_stops)
    add_fake_data(db, bus_2_data)


def add_fake_data(db, bus_data):
    for datum in bus_data:
        db.session.add(datum)
        db.session.commit()


def update_bus(db, bus):
    db.session.add(bus)
    db.session.commit()

