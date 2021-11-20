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
    assert data.find("</h2><a href=\"/logout\">Logout</a>") != -1


def test_login_show_message_incorrect_email(client):
    rv = client.post("/showSummary", data=dict(email='wrong@wrong.com'), follow_redirects=True)
    data = rv.data.decode()
    assert data.find("existe pas") != -1


def test_logout(client):
    rv = client.get("/logout", follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") != -1


def test_cannot_book_more_place_than_available_on_competition(client):
    """
    competition 'Big Wave' have 3 places available.
    club 'Iron Temple' have 4 points available.
    We try to book 4 places, but the competition have 3 places left.
    """
    rv = client.post(
        "/purchasePlaces",
        data=dict(club='Iron Temple', competition='Big Wave', places=4), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 404
    assert data.find("The competition have only 3 places left.") != -1


def test_can_book_place_available_on_competition(client):
    """
    competition 'Spring Festival' have 25 places available.
    club 'Iron Temple' have 4 points available.
    We book 4 places, and we have 4 places.
    """
    rv = client.post(
        "/purchasePlaces",
        data=dict(club='Iron Temple', competition='Spring Festival', places=4), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find('Great-booking complete!') != -1


def test_cannot_book_more_place_than_available_on_club(client):
   """
   competition 'Spring Festival' have 25 places available.
   club 'Iron Temple' have 4 points available.
   We try to book 10 places, but we have just 4 places.
   """
   rv = client.post(
       "/purchasePlaces",
       data=dict(club='Iron Temple', competition='Spring Festival', places=10), follow_redirects=True)
   data = rv.data.decode()
   assert rv.status_code == 404
   assert data.find("You do not have enough points.") != -1


def test_cannot_book_less_than_1_places_on_competition(client):
   """
   Try to enter a negative number to book some places on a competition.
   """
   rv = client.post(
       "/purchasePlaces",
       data=dict(club='Iron Temple', competition='Spring Festival', places=-10), follow_redirects=True)
   data = rv.data.decode()
   assert rv.status_code == 404
   assert data.find("You have to enter a positif number.") != -1
 

def test_cannot_book_more_than_12_places_on_competition(client):
   """
   Try to book more than 12 places on a competition.
   """
   rv = client.post(
       "/purchasePlaces",
       data=dict(club='Iron Temple', competition='Spring Festival', places=13), follow_redirects=True)
   data = rv.data.decode()
   assert rv.status_code == 404
   assert data.find("book more than 12 places.") != -1


def test_cannot_book_on_completed_competition(client):
    """
    competition 'Fall Classic' have 13 places available at 2020-10-22 13:30:00.
    club 'Iron Temple' have 4 points available.
    """
    rv = client.post(
        "/showSummary",data=dict(email='john@simplylift.co'), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find('<b>COMPLETED</b>') != -1


def test_club_place_decrease_on_booking_place_competition(client):
   """
   competition 'Spring Festival' have 25 places available.
   club 'Iron Temple' have 4 points available.
   We take 2 places, so we have 2 places left.
   """
   rv = client.post(
       "/purchasePlaces",
       data=dict(club='Iron Temple', competition='Spring Festival', places=2), follow_redirects=True)
   data = rv.data.decode()
   assert rv.status_code == 200
   assert data.find('Points available: 2') != -1


def test_show_list_competition_dashboard(client):
    rv = client.post("/showSummary", data=dict(email='john@simplylift.co'), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("Spring Festival<br />") != -1
    assert data.find("Fall Classic<br />") != -1
    assert data.find("Big Wave<br />") != -1


def test_show_list_club_dashboard(client):
    rv = client.post("/showClubs", data=dict(email='john@simplylift.co'), follow_redirects=True)
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("Simply Lift<br />") != -1
    assert data.find("Iron Temple<br />") != -1
    assert data.find("She Lifts<br />") != -1


