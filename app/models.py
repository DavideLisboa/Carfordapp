from . import db


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    sales_opportunity = db.Column(db.Boolean, default=True)
    cars = db.relationship('Car', backref='owner', lazy=True)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum('yellow', 'blue', 'gray',
                      name='car_colors'), nullable=False)
    model = db.Column(db.Enum('hatch', 'sedan', 'convertible',
                      name='car_models'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
