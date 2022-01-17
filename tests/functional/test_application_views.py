import pytest
from tests.functional.test_flask_petclinic import app
from tests.functional.test_flask_petclinic import client


@pytest.mark.usefixtures("app", "client")
def test_empty_db(client, app):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"<title>404 Not Found</title>" in rv.data
