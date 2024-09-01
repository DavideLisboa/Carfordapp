from flask import request, jsonify, Blueprint
from .models import Owner, Car
from .schemas import OwnerSchema, CarSchema
from .services import add_owner, add_car
from .utils import create_response
from flask_jwt_extended import jwt_required, create_access_token

# Initialize schemas
owner_schema = OwnerSchema()
car_schema = CarSchema()

# Create a blueprint

main = Blueprint('main', __name__)


@main.route('/owners', methods=['POST'])
@jwt_required()
def add_owner_route():
    data = request.json
    errors = owner_schema.validate(data)
    if errors:
        return create_response(message=errors, status=400)

    new_owner = add_owner(data['name'])
    return create_response(data=owner_schema.dump(new_owner), message="Owner added", status=201)


@main.route('/cars', methods=['POST'])
@jwt_required()
def add_car_route():
    data = request.json
    errors = car_schema.validate(data)
    if errors:
        return create_response(message=errors, status=400)

    new_car = add_car(data['color'], data['model'], data['owner_id'])
    if new_car:
        return create_response(data=car_schema.dump(new_car), message="Car added", status=201)
    return create_response(message="Cannot add car", status=400)


@main.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    cars = Car.query.all()
    return create_response(data=[car_schema.dump(car) for car in cars], status=200)


@main.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == 'password':
        access_token = create_access_token(
            identity={'username': data['username']})
        return create_response(data={"access_token": access_token}, message="Login successful", status=200)
    return create_response(message="Bad credentials", status=401)


def register_routes(app):
    app.register_blueprint(main)
