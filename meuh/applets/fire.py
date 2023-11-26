from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
ADMINPANELRESSOURCES = join(BASEDIR, 'admin_panel_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(ADMINPANELRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from attributions_changer import * # type: ignore 
from home import home

def fire(elem, method, form, args):

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
		conn.close()
		return users_asc, users_desc, users_asc_report, users_desc_report

	user_asc, user_desc, user_asc_report, user_desc_report = get_data()
	#make a connection to the database
	engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
	conn = engine.connect()

	users = get_all_usr(conn) # type: ignore
	#remove the current user from the list
	users = user_asc[0:10] # type: ignore
	dtlst = datalist("users", [user[0] for user in users], "usr") # type: ignore
	conn.close()

	content_udesc = "<table><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr>"
	for user in user_asc[0:10]:
		content_udesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td></tr>"
	content_udesc += "</table>"
	
	content_rdesc = "<table><tr><th>Username</th><th>Points</th><th>Extra Hours</th><th>Reports Count</th></tr>"
	for user in user_asc_report[0:10]:
		content_rdesc += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>"
	content_rdesc += "</table>"


	toadd = ""
	if method == 'POST':
		
		user = form['users']
		attr = form['attr']
		change_attr_lvl(user, attr, conn) # type: ignore
		
		
		toadd = Mk(f"""<div class="row gtr-uniform">
							<div class="col-12">
								<h3>Attribution changed</h3>
							</div>
						</div>""")
		
		if attr == "0":
			toadd = Mk(f"""<div class="row gtr-uniform">
							<div class="col-12">
								<h3>User deleted</h3>
							</div>
						</div>""")
								

   	#close 
	conn.close()

	elem['content'] = Mk(f"""   <section>
									<h3>Fire Someone!</h3>
					  				<span class="image fit"><img src="static/images/FIRE-SOMONE.gif" alt="pas trouvé"/></span>
					  				<p>Congratulations! You can choose a user to fire in the 10 worst employee!</p>
									{content_udesc} {content_rdesc}
									<form method="post">
	
										<div class="row gtr-uniform">
	
											{dtlst} 
											
											{selector_inc("attr",["None", "User", "Employee"], "Attribution")}
										
	
											{submit("Promote this employee to customer!")}
										</div>
									</form>
								</section>""") + toadd 
	
	return elem
