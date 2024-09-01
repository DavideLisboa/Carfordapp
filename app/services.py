from .models import Owner, Car
from . import db
import logging


def add_owner(name):
    new_owner = Owner(name=name)
    db.session.add(new_owner)
    db.session.commit()
    return new_owner


def add_car(color, model, owner_id):
    logging.info(
        f"Adding car with color={color}, model={model}, owner_id={owner_id}")
    owner = Owner.query.get(owner_id)
    if not owner:
        logging.error(f"Owner with ID {owner_id} not found.")
        return None
    if len(owner.cars) >= 3:
        logging.error(f"Owner with ID {owner_id} already has 3 cars.")
        return None
    new_car = Car(color=color, model=model, owner_id=owner_id)
    db.session.add(new_car)
    db.session.commit()
    owner.sales_opportunity = False
    db.session.commit()
    return new_car
