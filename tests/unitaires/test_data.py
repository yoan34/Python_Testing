from datetime import datetime
from data import loadClubs, loadCompetitions, loadTestCompetitions, loadTestClubs


def test_loadClubs():
    clubs = loadClubs()
    club1 = clubs[0]
    assert club1['name'] =='Simply Lift'
    assert club1['email'] == 'john@simplylift.co'
    assert club1['points'] == '13'
    assert len(clubs) == 3


def test_loadTestClubs():
    clubs = loadTestClubs()
    club1 = clubs[0]
    assert club1['name'] =='club1'
    assert club1['email'] == 'club1@test.com'
    assert club1['points'] == '13'
    assert len(clubs) == 3


def test_loadCompetitions():
    competitions = loadCompetitions()
    competition1 = competitions[0]
    assert competition1['name'] =='Spring Festival'
    assert competition1['date'] == datetime(2022, 3, 27, 10, 0 ,0)
    assert competition1['numberOfPlaces'] == '25'
    assert len(competitions) == 3


def test_loadTestCompetitions():
    competitions_test = loadTestCompetitions()
    competition1 = competitions_test[1]
    assert competition1['name'] =='competition2'
    assert competition1['date'] == datetime(2020,1,1)
    assert competition1['numberOfPlaces'] == '13'
    assert len(competitions_test) == 3