import socket

import pytest
from project.app_config.database import PetclinicApplication


@pytest.fixture(scope="session")
def app():
    """
    HALLO app
    """
    petclinic_application = PetclinicApplication(testing=True)
    app = petclinic_application.app
    app.config["TESTING"] = True
    app.testing = True
    app.port = app.config["PORT"]
    app.host = socket.gethostname()
    return app


@pytest.fixture(scope="session")
def client():
    """
    HALLO client
    """
    petclinic_application = PetclinicApplication(testing=True)
    app = petclinic_application.app
    app.config["TESTING"] = True
    app.testing = True
    app.port = app.config["PORT"]
    app.host = socket.gethostname()
    with app.test_client() as client:
        with app.app_context():
            db = petclinic_application.get_db()
        return client
