import json
import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         for competition in listOfCompetitions:
            date, hour = competition['date'].split(' ')
            y, m, d, h, s, ms = map(int, date.split('-') + hour.split(':'))
            new_date = datetime.datetime(y, m, d, h, s, ms)
            competition['date'] = new_date
         return listOfCompetitions


def loadTestClubs():
    return [
    {
        "name":"club1",
        "email":"club1@test.com",
        "points":"13"
    },
    {
        "name":"club2",
        "email": "club2@test.com",
        "points":"4"
    },
    {   "name":"club3",
        "email": "club3@test.com",
        "points":"12"
    }
]

def loadTestCompetitions():
    return [
        {
            "name": "competition1",
            "date": datetime.datetime.now() + datetime.timedelta(100),
            "numberOfPlaces": "25"
        },
        {
            "name": "competition2",
            "date": datetime.datetime(2020,1,1),
            "numberOfPlaces": "13"
        },
        {
            "name": "competition3",
            "date": datetime.datetime(2020,5,5),
            "numberOfPlaces": "3"
        }
    ]