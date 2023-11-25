from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
REPORTRESSOURCES = join(BASEDIR, 'report_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(REPORTRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore # type: ignore 
from home import home
from ressources import get_all_usr

def report(elem, method, form, args):

		#make a connection to the database
	engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
	conn = engine.connect()

	users = get_all_usr(conn) # type: ignore
	#remove the current user from the list
	users = [user for user in users if user[0] != elem['_usr']] # type: ignore
	dtlst = datalist("users", [user[0] for user in users], "usr") # 

	toadd = ""
	if method == "POST":

		toadd = f"""<p>Report sent!</p>
					<p>Thank you for your contribution!</p>"""

		#add the report to the database
		usr = form['usr']
	elem['content'] = Mk(f"""<section>
								<h3>Report</h3>
								an employee had done something wrong? report it here!
								<form method="post">
									<div class="row gtr-uniform">
                                            {dtlst}
											{selector_inc("attr",["None", "Miscellaneous", "Not Working", "Holidays", "Sickness", "Theft", "Early Leaves", "Other"], "type of report")}
											{txt("report", "report", "report")}
											{submit("Submit")}
									</div>
								</form>
							</section> {toadd}""")
	return elem
