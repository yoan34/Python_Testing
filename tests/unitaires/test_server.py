""" Server test """

import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client



def test_landing_page(client):
    rv = client.get('/', follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") != -1

def test_login_correct_email(client):
    rv = client.post("/showSummary", data=dict(email='john@simplylift.co'), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("<h2>Welcome,  </h2><a href=\"/logout\">Logout</a>") != -1

def test_login_show_message_incorrect_email(client):
    rv = client.post("/showSummary", data=dict(email='wrong@wrong.com'), follow_redirects=True)
    data = rv.data.decode()
    assert data.find("existe pas") != -1


