from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath

from meuh.applets.admin_panel_ressources.attributions_changer import change_rpt_status
from meuh.applets.ressources.buttons import selector_inc, submit

BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
ADMINPANELRESSOURCES = join(BASEDIR, 'admin_panel_ressources')
import sys

sys.path.append(RESSOURCES)
sys.path.append(ADMINPANELRESSOURCES)
sys.path.append(BASEDIR)
from buttons import *  # type: ignore
from attributions_changer import *  # type: ignore
from home import home


def adminpanel(elem, method, form, args):
    # make a connection to the database
    engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
    conn = engine.connect()

    users = get_all_usr(conn)  # type: ignore

    # remove the current user from the list
    users = [user for user in users if user[0] != elem['_usr']]  # type: ignore
    dtlst = datalist("users", [user[0] for user in users], "usr")  # type: ignore

    toadd = ""
    if method == 'POST':

        user = form['users']
        attr = form['attr']
        change_attr_lvl(user, attr, conn)  # type: ignore

        toadd = Mk(f"""<div class="row gtr-uniform">
                            <div class="col-12">
                                <h3>Attribution changed</h3>
                            </div>
                        </div>""")

        if attr == "0":
            toadd = Mk(f"""<div class="row gtr-uniform"><div class="col-12"><h3>User deleted</h3></div></div>""")

        status = form['status']
        conn.close()

        query = "SELECT id as ids,date AS d, report_type, accepted from reports WHERE accepted = 0 ORDER BY d DESC LIMIT 1"
        last_record = conn.execute(sql.text(query)).fetchone()
        id_record = last_record.ids


        if last_record:



            change_rpt_status(last_record.ids, status, conn)
            record_info = Mk(f"""<div class="row gtr-uniform"> <div class="col-12">
                                            <h3>Last warning</h3>
                                            <p>Date: {last_record.d}</p> <p>Report type: {last_record.report_type}</p>
                                        </div>
                                     </div>""")
        else:
            record_info = Mk("<p>Aucun enregistrement à afficher</p>")

    acceptance_field = selector_inc("accr", ["Refusé", "Accepté"], "Acceptation")

    # Ajout du champ de sélection pour Refusé/Accepté
    status_options = selector_inc("status", ["Refusé", "Accepté"], "Status")
    print(status_options)

    # Bouton Submit
    submit_button = submit("Submit")

    accbtn = submit("Reports")

    elem['content'] = Mk(f"""   <section>
                                    <h3>Admin panel</h3>
                                    
                                    <form method="post">
    
                                        <div class="row gtr-uniform">
    
                                            {dtlst} 
                                            
                                            {selector_inc("attr", ["None", "User", "Employee", "Admin", "Super User"], "Attribution")}
                                            
                                            {submit_button} 
                                            
                                            {record_info}
                                            
                                            {acceptance_field} 

                                            
                                            
                                            {accbtn}
                                            
                                        </div>
                                    </form>
                                </section>""") + toadd

    return elem
