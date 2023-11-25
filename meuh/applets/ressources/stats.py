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

    def create_table(users, title, report=False):
        if report:
            headers = "<tr><th>Username</th><th>Points</th><th>Reports Count</th></tr>"
        else:
            headers = "<tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"

        html_table = f"<table border='1' style='border-collapse: collapse; width: 50%; margin: 20px;'>"
        html_table += f"<caption><strong>{title}</strong></caption>"
        html_table += headers

        for user in users:
            if report:
                # Générer des lignes pour les tableaux de rapports
                html_table += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td></tr>"
            else:
                # Générer des lignes pour les autres tableaux
                html_table += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
        html_table += "</table>"
        return html_table

    # Création des quatre tableaux avec des titres
    table_asc_top = create_table(users_asc[:15], "Meilleurs (Haut)")
    table_desc_top = create_table(users_desc[:15], "Pires (Haut)")
    table_asc_bottom = create_table(users_asc_report[:15], "Meilleurs (Bas)", report=True)
    table_desc_bottom = create_table(users_desc_report[:15], "Pires (Bas)", report=True)

    # Combinaison des tableaux dans un seul conteneur HTML
    html = f"""
    <div style='display: flex; justify-content: space-around; align-items: flex-start; flex-wrap: nowrap; gap: 20px; overflow-x: auto;'>
        {table_asc_top}
        {table_desc_top}
        {table_asc_bottom}
        {table_desc_bottom}
    </div>
    """

    return html


# print(userlist())


engine = sql.create_engine('sqlite:///../databases/users.db', pool_pre_ping=True)
conn = engine.connect()

# Requête pour les données triées par ordre ascendant
query_asc = """UPDATE users 
SET 
    points = points / 10000;
"""
conn.execute(sql.text(query_asc))
conn.commit()

