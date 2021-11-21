import json
import datetime
from flask import Flask,render_template,request,redirect,flash,url_for

from data import loadClubs, loadCompetitions, loadTestCompetitions, loadTestClubs


def create_app(config):
    app = Flask(__name__)
    app.config.from_object('config')
    app.config["TESTING"] = config.get("TESTING")
    app.secret_key = 'something_special'
    if not app.config["TESTING"]:
        competitions = loadCompetitions()
        clubs = loadClubs()
    else:
        competitions = loadTestCompetitions()
        clubs = loadTestClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        club = [club for club in clubs if club['email'] == request.form['email']]
        if club:
            return render_template('welcome.html',club=club[0],competitions=competitions, date=datetime.datetime.now()), 200
        else:
            flash("Désolé, cet email n'existe pas.")
            return redirect(url_for('index'))


    @app.route('/showClubs',methods=['POST'])
    def showClubs():
        club = [club for club in clubs if club['email'] == request.form['email']]
        return render_template('clubs.html',club=club[0], clubs=clubs), 200

    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club]
        foundCompetition = [c for c in competitions if c['name'] == competition]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub[0],competition=foundCompetition[0])
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions, date=datetime.datetime.now())


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])


        # Condition pour me pas permettre de rentrer un nombre null ou négatif pour le nombre de place.
        if placesRequired <= 0:
           flash(f'You have to enter a positif number.')
           return render_template('booking.html',club=club,competition=competition), 404

        # Condition pour ne pas dépasser plus de 12 places à réserver.
        if placesRequired > 12:
           flash(f'You can\'t book more than 12 places.')
           return render_template('booking.html',club=club,competition=competition), 404

        # Condition permettant de regarder si le club à suffisament de points.
        if placesRequired > int(club['points']):
            flash(f'You do not have enough points. {club["points"]} availables.')
            return render_template('booking.html',club=club,competition=competition), 404

        # Condition permettant de voir si la competition à les places suffisante de la demande.
        if placesRequired > int(competition['numberOfPlaces']):
            flash(f'The competition have only {competition["numberOfPlaces"]} places left.')
            return render_template('booking.html',club=club,competition=competition), 404

        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club["points"] = str(int(club["points"]) - int(placesRequired))
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions, date=datetime.datetime.now())



    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app

app = create_app({"TESTING": False})


if __name__ == '__main__':
    app.run()