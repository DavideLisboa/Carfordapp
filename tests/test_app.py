import pytest
import json
import logging
import sys
from app import create_app, db
from app.models import Owner, Car

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def test_client():
    logger.debug("Setting up test client and in-memory database")
    app = create_app()
    app.config['TESTING'] = True
    # In-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
    logger.debug("Tearing down test client and database")


@pytest.fixture(scope='module')
def access_token(test_client):
    logger.debug("Requesting access token")
    response = test_client.post(
        '/login', json={'username': 'admin', 'password': 'password'})
    assert response.status_code == 200
    token = json.loads(response.data)['data']['access_token']
    logger.debug(f"Received access token: {token}")
    return token


def test_add_owner(test_client, access_token):
    logger.debug("Starting test_add_owner")
    response = test_client.post('/owners',
                                json={'name': 'John Doe'},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding owner: {response.data}")
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['name'] == 'John Doe'
    assert data['data']['sales_opportunity'] is True
    logger.debug("Completed test_add_owner")


def test_add_car(test_client, access_token):
    logger.debug("Starting test_add_car")
    # First, create an owner
    response = test_client.post('/owners',
                                json={'name': 'Jane Doe'},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding owner: {response.data}")
    owner = Owner.query.first()
    assert owner is not None

    # Add a car
    response = test_client.post('/cars',
                                json={'color': 'blue', 'model': 'hatch',
                                      'owner_id': owner.id},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding car: {response.data}")
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['color'] == 'blue'
    assert data['data']['model'] == 'hatch'
    assert data['data']['owner_id'] == owner.id
    logger.debug("Completed test_add_car")


def test_add_car_without_owner(test_client, access_token):
    logger.debug("Starting test_add_car_without_owner")
    # Try to add a car without an owner
    response = test_client.post('/cars',
                                json={'color': 'blue',
                                      'model': 'hatch', 'owner_id': 9999},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding car without owner: {response.data}")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == "Cannot add car"
    logger.debug("Completed test_add_car_without_owner")


def test_add_car_with_invalid_color(test_client, access_token):
    logger.debug("Starting test_add_car_with_invalid_color")
    # Create an owner
    response = test_client.post('/owners',
                                json={'name': 'Alice Doe'},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding owner: {response.data}")
    owner = Owner.query.first()
    assert owner is not None

    # Try to add a car with an invalid color
    response = test_client.post('/cars',
                                json={'color': 'purple',
                                      'model': 'hatch', 'owner_id': owner.id},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(
        f"Response for adding car with invalid color: {response.data}")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'color' in data['message']
    logger.debug("Completed test_add_car_with_invalid_color")


def test_add_car_with_invalid_model(test_client, access_token):
    logger.debug("Starting test_add_car_with_invalid_model")
    # Create an owner
    response = test_client.post('/owners',
                                json={'name': 'Bob Doe'},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(f"Response for adding owner: {response.data}")
    owner = Owner.query.first()
    assert owner is not None

    # Try to add a car with an invalid model
    response = test_client.post('/cars',
                                json={'color': 'blue', 'model': 'truck',
                                      'owner_id': owner.id},
                                headers={'Authorization': f'Bearer {access_token}'})
    logger.debug(
        f"Response for adding car with invalid model: {response.data}")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'model' in data['message']
    logger.debug("Completed test_add_car_with_invalid_model")


if __name__ == "__main__":
    logger.debug("Running tests from main")
    sys.exit(pytest.main())
