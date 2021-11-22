""" Server test """

import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


class TestHome:

    def test_reach_index_page(self, client):
        rv = client.get('/', follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("Welcome to the GUDLFT Registration Portal!") != -1

    def test_login_correct_email(self, client):
        rv = client.post("/showSummary", data=dict(email='club1@test.com'), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("</h2><a class=\"logout\" href=\"/logout\">Logout</a>") != -1

    def test_login_show_message_incorrect_email(slef, client):
        rv = client.post("/showSummary", data=dict(email='wrong@wrong.com'), follow_redirects=True)
        data = rv.data.decode()
        assert data.find("existe pas") != -1


class TestShowSummary:

    def test_reach_showSummary_page(self, client):
        rv = client.post('/showSummary',data=dict(email='club1@test.com'), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("<h2>Welcome, club1@test.com </h2><a class=\"logout\" href=\"/logout\">Logout</a>") != -1

    def test_logout(self, client):
        rv = client.get("/logout", follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("Welcome to the GUDLFT Registration Portal!") != -1

    def test_cannot_book_on_completed_competition(self, client):
        """
        competition 'Fall Classic' have 13 places available at 2020-10-22 13:30:00.
        club 'Iron Temple' have 4 points available.
        """
        rv = client.post(
            "/showSummary",data=dict(email='club1@test.com'), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("""competition2<br />
            Date: 2020-01-01 00:00:00</br>
            Number of Places: 13
            
                <b>COMPLETED</b>""") != -1

    def test_show_list_competitions(self, client):
        rv = client.post("/showSummary", data=dict(email='club1@test.com'), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("competition1<br />") != -1
        assert data.find("competition2<br />") != -1
        assert data.find("competition3<br />") != -1

    def test_show_list_clubs(self, client):
        rv = client.post("/showClubs", data=dict(email='club1@test.com'), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find("club1<br />") != -1
        assert data.find("club2<br />") != -1
        assert data.find("club3<br />") != -1


class TestBook:

    def test_reach_boook_page(self, client):
        rv = client.get('/book/competition1/club1', follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find('<title>Booking for competition1 || GUDLFT</title>') != -1
        assert data.find('<label for="places">How many places?</label><input type="number" name="places" id=""/>') != -1

    def test_not_found(self, client):
        rv = client.get("/book/competition1/club", follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find('<li>Something went wrong-please try again</li>') != -1


class TestPurchasePlaces:

    def test_cannot_book_more_place_than_available_on_competition(self, client):
        """
        competition 'competition3' have 3 places available.
        club 'club1' have 4 points available.
        We try to book 4 places, but the competition have 3 places left.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club1', competition='competition3', places=4), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 404
        assert data.find("The competition have only 3 places left.") != -1

    def test_can_book_place_available_on_competition(self, client):
        """
        competition 'competition1' have 25 places available.
        club 'club2' have 4 points available.
        We book 4 places, and we have 4 places.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club2', competition='competition1', places=4), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find('Great-booking complete!') != -1

    def test_cannot_spend_more_points_than_available_on_club(self, client):
        """
        competition 'competition1' have 25 places available.
        club 'club2' have 4 points available.
        We try to book 10 places, but we have just 4 places.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club2', competition='competition1', places=10), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 404
        assert data.find("You do not have enough points.") != -1

    def test_cannot_book_less_than_1_places_on_competition(self, client):
        """
        Try to enter a negative number to book some places on a competition.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club2', competition='competition1', places=-10), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 404
        assert data.find("You have to enter a positif number.") != -1

    def test_cannot_book_more_than_12_places_on_competition(self, client):
        """
        Try to book more than 12 places on a competition.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club1', competition='competition1', places=13), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 404
        assert data.find("book more than 12 places.") != -1

    def test_club_place_decrease_on_booking_place_competition(self, client):
        """
        competition 'competition1' have 25 places available.
        club 'club2' have 4 points available.
        We take 2 places, so we have 2 places left.
        """
        rv = client.post(
            "/purchasePlaces",
            data=dict(club='club2', competition='competition1', places=2), follow_redirects=True)
        data = rv.data.decode()
        assert rv.status_code == 200
        assert data.find('Points available: 2') != -1








