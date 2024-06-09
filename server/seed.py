#!/usr/bin/env python3

from app import app, db
from models import Plant

with app.app_context():
    Plant.query.delete()

    aloe = Plant(
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
    )

    db.session.add_all([aloe, zz_plant])
    db.session.commit()