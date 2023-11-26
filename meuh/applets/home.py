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

        query_asc_report = """SELECT u.username, u.points, u.extra_hours, COUNT(r.user_id) 
                            FROM users AS u 
                            LEFT JOIN reports AS r ON u.id = r.user_id
                            GROUP BY u.id, u.username, u.points 
                            ORDER BY u.points ASC
                            LIMIT 10"""
        users_asc_report = conn.execute(sql.text(query_asc_report)).fetchall()

        # Requête pour les données triées par ordre descendant
        query_desc = "SELECT username, points, sick_days, holidays, late_hours FROM users ORDER BY points DESC"
        users_desc = conn.execute(sql.text(query_desc)).fetchall()

        query_desc_report = """SELECT u.username, u.points, u.extra_hours, COUNT(r.user_id) 
                            FROM users AS u 
                            LEFT JOIN reports AS r ON u.id = r.user_id
                            GROUP BY u.id, u.username, u.points 
                            ORDER BY u.points DESC
                            LIMIT 10"""
        users_desc_report = conn.execute(sql.text(query_desc_report)).fetchall()

        return users_asc, users_desc, users_asc_report, users_desc_report
    # Fetch user stats

    elem['search'] = Mk(f"""Hello there ! you are logged in as {elem['_usr']}.""")

    if not elem['_attr_lvl']:
        elem['search'] = Mk(
            """Hello there ! you are not logged in. Please log in or sign up to access the full content of this website.""")

    user_asc, user_desc, user_asc_report, user_desc_report = get_data()
    # Create tables
    content_uasc = "<table><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
    for user in user_asc[0:10]:
        content_uasc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
    content_uasc += "</table>"

    content_udesc = "<table><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
    for user in user_desc[0:10]:
        content_udesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
    content_udesc += "</table>"

    content_rasc = "<table><tr><th>Username </th><th>Points</th><th>Extra Hours</th><th>Reports Count</th></tr>"
    for user in user_asc_report[0:10]:
        content_rasc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>"
    content_rasc += "</table>"

    content_rdesc = "<table><tr><th>Username</th><th>Points</th><th>Extra Hours</th><th>Reports Count</th></tr>"
    for user in user_desc_report[0:10]:
        content_rdesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>"
    content_rdesc += "</table>"

    from math import floor
    to_add =""
    congrats = ""
    try:
        if elem['_attr_lvl']:
            #get the Username	Points	Sick Days	Holidays	Late Hours extra hours
            engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
            conn = engine.connect()
            query = f"SELECT username, points, sick_days, holidays, late_hours, extra_hours FROM users WHERE username = '{elem['_usr']}'"
            user = conn.execute(sql.text(query)).fetchall()[0]
            all_users_means = conn.execute(sql.text("SELECT AVG(points), AVG(sick_days), AVG(holidays), AVG(late_hours), AVG(extra_hours) FROM users")).fetchall()[0]
            conn.close()

            if user[0] == user_desc[0][0]:
                congrats = f"""
                        <img src="static/images/e6872035363c418f1a74d5da89592791.gif" alt="pas trouvé" style="width: 20%;"/>
                        <h4> You are the employee of the month !</h4> <br/>
                        <h5> You won the chance to promote someone to customer !</h5>
                """


            to_add = f"""
                    <h4>
                    <br/>
                    <br/>
                    <strong>Your stats</strong><br/>
                    Username: {user[0]}<br/>
                    Points (mean of the company): {user[1]} <strong>({floor(all_users_means[0])})</strong><br/>
                    Sick Days (mean of the company): {user[2]} <strong>({floor(all_users_means[1])})</strong><br/>
                    Holidays (mean of the company): {user[3]} <strong>({floor(all_users_means[2])})</strong><br/>
                    Late Hours (mean of the company): {user[4]} <strong>({floor(all_users_means[3])})</strong><br/>
                    Extra Hours (mean of the company): {user[5]} <strong>({floor(all_users_means[4])})</strong><br/>
                    <br/>
                    <br/>
                    </h4>"""
    except:
        pass
    # elem['content'] = Mk("")

    elem['content'] = Mk(f"""
    {congrats}
    <br/>
    <h1>Worst employee of the month is {user_asc[0][0]}</h1>
    <h1>Collabo of the month is {user_desc[0][0]}</h1>
    <div class="row gtr-uniform">
        <div class="col-8">
            {to_add}
        </div>
        <div class="col-4">
        </div>
    </div>
    <div class="row gtr-uniform">
        <div class="col-5">
            <img src="static/images/BAD-BOY.gif" alt="pas trouvé" style="width: 100%;"/>
        </div>

        <div class="col-2">
        </div>

        <div class="col-5">
            <img src="static/images/good-boy.gif" alt="pas trouvé" style="width: 100%;"/>
        </div>

        <div class="col-5">
            {content_uasc}
        </div>

        <div class="col-2" style="display: flex; align-items: center;">
            <img src="static/images/giphy2.gif" alt="pas trouvé" style="width: 100%;"/>
        </div>

        <div class="col-5">
            {content_udesc}
        </div>

        <div class="col-5">
            {content_rasc}
        </div>

        <div class="col-2">
        </div>

        <div class="col-5">
            {content_rdesc}
        </div>

    </div>""")





    return elem
