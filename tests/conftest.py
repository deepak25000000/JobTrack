import pytest

from app import create_app
from extensions import db


@pytest.fixture
def client():

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key-for-jobtrack-testing-1234567890"
    })

    with app.app_context():

        db.create_all() #this is not used in app.py because whenever we start our flask application it also starts the database with new values 

        yield app.test_client()

        db.session.remove()
        db.drop_all()

