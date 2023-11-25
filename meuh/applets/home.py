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
    # Fetch user stats

    elem['search'] = Mk(f"""Hello there ! you are logged in as {elem['_usr']}.""")

    if not elem['_attr_lvl']:
        elem['search'] = Mk(
            """Hello there ! you are not logged in. Please log in or sign up to access the full content of this website.""")

    # elem['content'] = Mk("")

    elem['content'] = Mk("""<div style='display: flex; justify-content: space-around; align-items: flex-start; flex-wrap: nowrap; gap: 20px; overflow-x: auto;'>
        <table border='1' style='border-collapse: collapse; width: 50%; margin: 20px;'><caption><strong>Meilleurs (Haut)</strong></caption><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr><tr><td>Mackintosh</td><td>300000000</td><td>5</td><td>10</td><td>24</td></tr><tr><td>Samuela</td><td>700000000</td><td>7</td><td>25</td><td>55</td></tr><tr><td>Lorene</td><td>900000000</td><td>9</td><td>11</td><td>37</td></tr><tr><td>Haukom</td><td>1400000000</td><td>1</td><td>5</td><td>49</td></tr><tr><td>Aires</td><td>1500000000</td><td>0</td><td>18</td><td>74</td></tr><tr><td>Nea</td><td>2200000000</td><td>7</td><td>6</td><td>7</td></tr><tr><td>Conard</td><td>2300000000</td><td>8</td><td>14</td><td>19</td></tr><tr><td>Gamal</td><td>2300000000</td><td>1</td><td>28</td><td>35</td></tr><tr><td>Medrek</td><td>3200000000</td><td>0</td><td>22</td><td>58</td></tr><tr><td>Mages</td><td>3600000000</td><td>6</td><td>29</td><td>73</td></tr><tr><td>Jaret</td><td>5200000000</td><td>8</td><td>16</td><td>38</td></tr><tr><td>Leon</td><td>5800000000</td><td>6</td><td>10</td><td>12</td></tr><tr><td>Parnell</td><td>5900000000</td><td>5</td><td>29</td><td>69</td></tr><tr><td>Bandler</td><td>6000000000</td><td>1</td><td>11</td><td>35</td></tr><tr><td>Yvon</td><td>6000000000</td><td>5</td><td>4</td><td>68</td></tr></table>
        <table border='1' style='border-collapse: collapse; width: 50%; margin: 20px;'><caption><strong>Pires (Haut)</strong></caption><tr><th>Username</th><th>Points</th><th>Sick Days</th><th>Holidays</th><th>Late Hours</th></tr><tr><td>admin</td><td>10000000000000</td><td>10</td><td>30</td><td>100</td></tr><tr><td>Nereus</td><td>9999100000000</td><td>1</td><td>27</td><td>46</td></tr><tr><td>Patnode</td><td>9997900000000</td><td>4</td><td>1</td><td>83</td></tr><tr><td>Bratton</td><td>9997200000000</td><td>6</td><td>1</td><td>24</td></tr><tr><td>Kawai</td><td>9997200000000</td><td>10</td><td>24</td><td>29</td></tr><tr><td>Burrton</td><td>9996800000000</td><td>6</td><td>5</td><td>51</td></tr><tr><td>Zaremski</td><td>9996100000000</td><td>5</td><td>30</td><td>36</td></tr><tr><td>Femmine</td><td>9995100000000</td><td>9</td><td>17</td><td>57</td></tr><tr><td>Kenzie</td><td>9992300000000</td><td>1</td><td>17</td><td>68</td></tr><tr><td>Parker</td><td>9991200000000</td><td>10</td><td>19</td><td>56</td></tr><tr><td>Gabey</td><td>9990800000000</td><td>9</td><td>8</td><td>43</td></tr><tr><td>Aviva</td><td>9988000000000</td><td>8</td><td>0</td><td>43</td></tr><tr><td>Shandee</td><td>9988000000000</td><td>1</td><td>20</td><td>93</td></tr><tr><td>Rebba</td><td>9987300000000</td><td>10</td><td>11</td><td>52</td></tr><tr><td>Shaffert</td><td>9987200000000</td><td>1</td><td>13</td><td>23</td></tr></table>
        <table border='1' style='border-collapse: collapse; width: 50%; margin: 20px;'><caption><strong>Meilleurs (Bas)</strong></caption><tr><th>Username</th><th>Points</th><th>Reports Count</th></tr><tr><td>Mackintosh</td><td>300000000</td><td>1</td></tr><tr><td>Samuela</td><td>700000000</td><td>2</td></tr><tr><td>Lorene</td><td>900000000</td><td>1</td></tr><tr><td>Haukom</td><td>1400000000</td><td>1</td></tr><tr><td>Aires</td><td>1500000000</td><td>1</td></tr><tr><td>Nea</td><td>2200000000</td><td>3</td></tr><tr><td>Conard</td><td>2300000000</td><td>1</td></tr><tr><td>Gamal</td><td>2300000000</td><td>2</td></tr><tr><td>Medrek</td><td>3200000000</td><td>3</td></tr><tr><td>Mages</td><td>3600000000</td><td>5</td></tr><tr><td>Jaret</td><td>5200000000</td><td>2</td></tr><tr><td>Leon</td><td>5800000000</td><td>1</td></tr><tr><td>Yvon</td><td>6000000000</td><td>1</td></tr><tr><td>Gagnon</td><td>7400000000</td><td>1</td></tr><tr><td>Harpp</td><td>8100000000</td><td>2</td></tr></table>
        <table border='1' style='border-collapse: collapse; width: 50%; margin: 20px;'><caption><strong>Pires (Bas)</strong></caption><tr><th>Username</th><th>Points</th><th>Reports Count</th></tr><tr><td>admin</td><td>10000000000000</td><td>1</td></tr><tr><td>Nereus</td><td>9999100000000</td><td>3</td></tr><tr><td>Patnode</td><td>9997900000000</td><td>1</td></tr><tr><td>Bratton</td><td>9997200000000</td><td>1</td></tr><tr><td>Kawai</td><td>9997200000000</td><td>1</td></tr><tr><td>Burrton</td><td>9996800000000</td><td>4</td></tr><tr><td>Zaremski</td><td>9996100000000</td><td>3</td></tr><tr><td>Femmine</td><td>9995100000000</td><td>4</td></tr><tr><td>Parker</td><td>9991200000000</td><td>3</td></tr><tr><td>Gabey</td><td>9990800000000</td><td>5</td></tr><tr><td>Aviva</td><td>9988000000000</td><td>1</td></tr><tr><td>Shandee</td><td>9988000000000</td><td>1</td></tr><tr><td>Rebba</td><td>9987300000000</td><td>2</td></tr><tr><td>Shaffert</td><td>9987200000000</td><td>3</td></tr><tr><td>Raab</td><td>9987100000000</td><td>1</td></tr></table>
    </div>""")





    return elem
