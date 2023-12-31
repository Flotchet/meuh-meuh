# Dynamic web app for the Meuh Meuh, your HR assistant! project
# Author: Meuh Meuh Corporation

# Dynamic import of applets and configuration files

from __future__ import annotations

from os import listdir
from os.path import join, dirname, abspath
from importlib import import_module

import sqlalchemy as sql
from constructors import elements
BASEDIR = abspath(dirname(__file__))
APPLETDIR = join(BASEDIR, 'applets')
CONFIGDIR = join(BASEDIR, 'config')

applets = [f[:-3] for f in listdir(APPLETDIR) if f.endswith('.py')]
applets.sort()
#import all applets
for applet in applets:
    import_module(f'applets.{applet}')

#make a dictionary of all applets's attributes
applets_attr = {applet: getattr(import_module(f'applets.{applet}'), applet) for applet in applets}

def ini_reader(location : str) -> dict():

    """Reads an ini file and returns a dictionary with the values"""
    # This function reads an ini file and returns a dictionary with the values

    with open(location, "r") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if not(line.startswith("#"))]
    lines = [line.split("=") for line in lines if not(line == "")]
    lines = [(line[0].strip(), line[1].strip()) for line in lines]

    return dict(lines)

applets_ini = {applet: ini_reader(join(CONFIGDIR, f'{applet}.ini')) for applet in applets}

# imports

from flask import Flask, render_template, request, url_for, session, Response, g, redirect, Markup as Mk
from waitress import serve
import secrets


#print applet attributes
for applet in applets:
    print(applet, applets_attr[applet])

# app configuration

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

UPLOAD_FOLDER = 'uploads'
ALLOWED_DATA_EXTENSIONS = {'csv', 'db', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["DEBUG"] = True
app.config["SESSION_TYPE"] = "filesystem"


def menu(element : dict) -> Markup: # type: ignore 
    """This function returns the menu"""
    # This function returns the menu

    menu = """
    <nav id="menu">
	    <header class="major">
			<h2>Menu</h2>
		</header>
        <ul>
        """
            
    for applet in applets:
        if int(applets_ini[applet]['min_lvl']) <= element['_attr_lvl'] <= int(applets_ini[applet]['max_lvl']):
            menu += f"""
            <li><a href="/{applet}">{applets_ini[applet]['name']}</a></li>
            """
    menu += """
        </ul>
    </nav>
    <nav>
    """

    return Mk(menu)



@app.route('/<applet>', methods = ['GET', 'POST', 'PUT', 'DELETE', 'SUPER'])
def core(applet = None):

    try:
        elem = session['elem']

    except:
        elem = elements(applets = applets_attr.keys(), authors = "Meuh Meuh Corporation")
        elem = elem()
        session['elem'] = elem
        session['last_applet'] = applet

    try:
        #try to call the applet and pass the elem object and the methods
        elem = applets_attr[applet](elem, request.method, request.form, request.args)
        session['elem'] = elem
        if not int(applets_ini[applet]['min_lvl']) <= elem['_attr_lvl'] <= int(applets_ini[applet]['max_lvl']):
            print("not in range")
            return redirect(url_for('core', applet = 'home'), code=302)
        
    
    except:
        return redirect(url_for('core', applet = 'home'), code=302)

    #check if all the attributes are present
    if not all([attr in elem.keys() for attr in ['head', 'header', 'menu', 'content', 'side_content', 'search', 'side_footer', 'scripts']]):
        #if not, return the home page
        elem = applets_attr['home'](elem, request.method, request.form, request.args)
        session['elem'] = elem

    try:
        session['last_elem']
    except:
        session['last_elem'] = elem

    #if the applet has changed
    if applet != session['last_applet']:
        #check if the content has changed
        if elem['content'] == session['last_elem']['content']:
            #if not, return the last page
            redirect(url_for('core', applet = 'home'), code=302)

        if elem['side_content'] == session['last_elem']['side_content']:
            #if not, return the last page
            from flask import Markup as MK
            from math import floor
            to_add =""
            if elem['_attr_lvl']:
                #get the Username	Points	Sick Days	Holidays	Late Hours extra hours
                engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'applets/databases/users.db'))
                conn = engine.connect()
                query = f"SELECT username, points, sick_days, holidays, late_hours, extra_hours FROM users WHERE username = '{elem['_usr']}'"
                user = conn.execute(sql.text(query)).fetchall()[0]
                all_users_means = conn.execute(sql.text("SELECT AVG(points), AVG(sick_days), AVG(holidays), AVG(late_hours), AVG(extra_hours) FROM users")).fetchall()[0]
                conn.close()
                to_add = f"""
                            <br/>
                            <br/>
                            <strong>Your stats</strong><br/>
                            Username: {user[0]}<br/>
                            Points: {user[1]} <strong>({floor(all_users_means[0])})</strong><br/>
                            Sick Days: {user[2]} <strong>({floor(all_users_means[1])})</strong><br/>
                            Holidays: {user[3]} <strong>({floor(all_users_means[2])})</strong><br/>
                            Late Hours: {user[4]} <strong>({floor(all_users_means[3])})</strong><br/>
                            Extra Hours: {user[5]} <strong>({floor(all_users_means[4])})</strong><br/>"""

            elem['side_content'] = MK(to_add + '<br/><div class="row gtr-uniform"><div class="col-9"><span class="image fit"><img src="static/images/polish-cow-dancing-cow.gif" alt="pas trouvé"/></span> </div></div>')

    

    elem['menu'] = menu(elem)
    session['last_elem'] = elem
    session['last_applet'] = applet



    return render_template('base.html',
        head = elem['head'],
        header =elem['header'],
        menu = elem['menu'],
        content =elem['content'],
        side_content = elem['side_content'],
        search = elem['search'] ,
        side_footer = elem['side_footer'] ,
        scripts = elem['scripts']

    )

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('core', applet = 'home'), code=302)


#serve(app, host="0.0.0.0", port=8080)
app.run()
