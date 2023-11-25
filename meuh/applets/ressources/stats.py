
import sqlalchemy as sql

from os.path import join, dirname, abspath

BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
ADMINPANELRESSOURCES = '../admin_panel_ressources'
import sys

sys.path.append(RESSOURCES)
sys.path.append(ADMINPANELRESSOURCES)
sys.path.append(BASEDIR)
from buttons import *  # type: ignore
from attributions_changer import *  # type: ignore


def userlist():
    # Connexion à la base de données
    engine = sql.create_engine('sqlite:///../databases/users.db', pool_pre_ping=True)
    conn = engine.connect()

    # Requête pour les données triées par ordre ascendant
    query_asc = "SELECT username, points, sick_days, holidays, late_hours FROM users ORDER BY points ASC"
    users_asc = conn.execute(sql.text(query_asc)).fetchall()



    # Requête pour les données triées par ordre descendant
    query_desc = "SELECT username, points, sick_days, holidays, late_hours FROM users ORDER BY points DESC"
    users_desc = conn.execute(sql.text(query_desc)).fetchall()

    # Fonction pour créer un tableau HTML
    def create_table(users):
        html_table = "<table border='1'>"
        html_table += "<tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
        for user in users:
            html_table += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
        html_table += "</table>"
        return html_table

    # Création des deux tableaux
    table_asc = create_table(users_asc[:15])
    table_desc = create_table(users_desc[:15])

    # Combinaison des deux tableaux dans un conteneur HTML
    html = f"<div style='display: flex; justify-content: space-around;'>{table_asc}{table_desc}</div>"

    return html

print(userlist())


