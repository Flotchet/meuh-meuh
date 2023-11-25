from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
SIGNUPRESSOURCES = join(BASEDIR, 'sign_up_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(SIGNUPRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore
from create_user import * # type: ignore


def signup(elem, method, form, args):
    
	test = ""
	if method == 'POST':

		username = form['id']
		password = form['password']
		password2 = form['password2']
		#create engine

		engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
		conn = engine.connect()
		

		test = create_user(username, password, password2, conn) # type: ignore


		conn.close()
	


	elem['content'] = Mk(f"""       <section>
									<div class="row gtr-uniform">
									<div class="col-2">
									</div>
										<div class="col-8">
											<span class="image fit"><img src="static/images/MEUH MEUH WANTS YOU.png" alt="pas trouvé"/></span>
											{breaker()}
										</div>
									<div class="col-2">
									</div>
									</div>
									<h3>Sign up</h3>
									
									<form method="post">
	
										<div class="row gtr-uniform">
	
											{logger("Username")}

											{breaker()}

											{pwd("password2", "repeat password")}
	
											{submit("Sign up")}

										</div>
									</form>
									{test}
								</section>""")
	return elem
