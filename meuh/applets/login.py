from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
LOGINRESSOURCES = join(BASEDIR, 'login_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(LOGINRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from check_user import * # type: ignore 
from home import home

def login(elem, method, form, args):

	toadd = ""
	if method == 'POST':
		
		username = form['id']
		password = form['password']
		#create engine
		engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
		conn = engine.connect()
		
		elem['_attr_lvl'] = check_user(username, password, conn) # type: ignore 

		conn.close()
		elem['_usr'] = username	

		if elem['_attr_lvl'] == 0:
			toadd = Mk(f"""<p>Wrong username or password</p>""")
			elem['_usr'] = ""	
			
			
   
	elem['content'] = Mk(f"""       <section>
									<h3>Log In</h3>
					  				<img src="static/images/LOGIN.gif" alt="pas trouvé" style="width: 100%;"/>
									
									<form method="post" >
	
										<div class="row gtr-uniform">
	
											{logger("Username")} 
										
	
											{submit("Log In")}
										</div>
									</form>
								</section>""") + toadd 
	
	return elem
