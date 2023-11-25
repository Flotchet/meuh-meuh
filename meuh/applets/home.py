from flask import Markup as Mk

from os.path import join, dirname, abspath
import sqlalchemy as sql

BASEDIR = abspath(dirname(__file__))
ADMINPANELRESSOURCES = join(BASEDIR, 'admin_panel_ressources')
RESSOURCES = join(BASEDIR, 'ressources')
import sys

sys.path.append(RESSOURCES)
sys.path.append(ADMINPANELRESSOURCES)
sys.path.append(BASEDIR)
from buttons import *  # type: ignore
from attributions_changer import *  # type: ignore


def home(elem, method, form, args):
    def get_data():
        # Connexion à la base de données
        engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
        conn = engine.connect()

        # Requête pour les données triées par ordre ascendant
        query_asc = "SELECT username, points, sick_days, holidays, late_hours FROM users ORDER BY points ASC"
        users_asc = conn.execute(sql.text(query_asc)).fetchall()

        query_asc_report = """SELECT u.username, u.points, COUNT(r.user_id2) 
                            FROM users AS u 
                            INNER JOIN reports AS r ON u.id = r.user_id2 
                            GROUP BY u.id, u.username, u.points 
                            ORDER BY u.points ASC"""
        users_asc_report = conn.execute(sql.text(query_asc_report)).fetchall()

        # Requête pour les données triées par ordre descendant
        query_desc = "SELECT username, points, sick_days, holidays, late_hours FROM users ORDER BY points DESC"
        users_desc = conn.execute(sql.text(query_desc)).fetchall()

        query_desc_report = """SELECT u.username, u.points, COUNT(r.user_id2) 
                            FROM users AS u 
                            INNER JOIN reports AS r ON u.id = r.user_id2 
                            GROUP BY u.id, u.username, u.points 
                            ORDER BY u.points DESC"""
        users_desc_report = conn.execute(sql.text(query_desc_report)).fetchall()

        return users_asc, users_desc, users_asc_report, users_desc_report
    # Fetch user stats

    elem['search'] = Mk(f"""Hello there ! you are logged in as {elem['_usr']}.""")

    if not elem['_attr_lvl']:
        elem['search'] = Mk(
            """Hello there ! you are not logged in. Please log in or sign up to access the full content of this website.""")

    user_asc, user_desc, user_asc_report, user_desc_report = get_data()
    # Create tables
    content_uasc = "<table border='5' style='width: 500;'><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
    for user in user_asc[0:10]:
        content_uasc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
    content_uasc += "</table>"

    content_udesc = "<table border='5' style='width: 500px;'><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
    for user in user_desc[0:10]:
        content_udesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
    content_udesc += "</table>"

    content_rasc = "<table border='5' style='width: 500px;'><tr><th>Username </th><th>Points</th><th>Reports Count</th></tr>"
    for user in user_asc_report[0:10]:
        content_rasc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td></tr>"
    content_rasc += "</table>"

    content_rdesc = "<table border='5' style='width: 500px;'><tr><th>Username</th><th>Points</th><th>Reports Count</th></tr>"
    for user in user_desc_report[0:10]:
        content_rdesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td></tr>"
    content_rdesc += "</table>"



    # elem['content'] = Mk("")

    elem['content'] = Mk(f"""
    <div class="row gtr-uniform">

        <div class="col-6">
            <h3>Top 10 Meilleurs</h3>
            {content_uasc}
        </div>

        <div class="col-6">
            <h3>Top 10 Pires</h3>
            {content_udesc}
        </div>

        <div class="col-6">
            {content_rasc}
        </div>

        <div class="col-6">
            {content_rdesc}
        </div>

    </div>""")





    return elem
