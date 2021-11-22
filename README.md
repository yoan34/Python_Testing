# gudlift-registration

Liste des différentes étapes pour récupérer et lancer le projet:

- <code>git clone https://github.com/yoan34/Python_Testing.git</code>
- <code>cd Python_testing</code>
- <code>python3 -m venv env</code> : Permet de créer un environement virtuel.
- <code>. env/bin/activate</code> : Active l'environnement virtuel sur MacOS/Linux.
- <code>pip install -r requirements.txt</code> : Installe les dépendances nécessaires au projet.


Pour lancer l'application:
- <code>git checkout QA></code> : Se positionner sur la branche QA qui n'est pas merge avec la master, c'est la branche la plus avancée qui attend une validation.
- <code>export FLASK_APP=server.py</code> : à faire qu'une fois
- <code>export FLASK_TESTING=False</code> : à faire que si la variable est à True aprês avoir fait les tests.
- <code>flask run</code>

Pour lancer les tests:
- <code>git checkout QA></code> :Aller sur la branche QA.
- <code>export FLASK_TESTING=True</code> : Permet au test fonctionnel d'utiliser les données de test une fois le serveur lancé.
- <code>pytest -v</code>


Pour avoir un rapport sur la couverture des tests:
- <code>git checkout QA></code> Aller sur la branche QA.
- <code>pytest --cov=.</code>
- <code>pytest --cov=. --cov-html html</code> : Créé un rapport HTML à la racine du projet.


Pour voir la performance avec Locust:
- <code>git checkout QA></code> :Aller sur la branche QA.
- <code>locust -f tests/performance_tests/locustfile.py</code>
- Se connecter à l'adresse **http://0.0.0.0:8089/** et entrer 1 user, 1 spwan rate à l'url http://0.0.0.0:5000 et cliqué sur start swarming.


