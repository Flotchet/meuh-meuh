import sqlalchemy
import hashlib


def check_user(username, password, conn) :
        print("Checking user")
        #check if the user exists
        if not conn.execute(sqlalchemy.text(f"""SELECT EXISTS(SELECT 1 FROM users WHERE username = '{username}')""")).fetchone()[0]:
            print("User does not exist")
            return 0
    
        #check if the password is correct
        if conn.execute(sqlalchemy.text(f"""SELECT password FROM users WHERE username = '{username}'""")).fetchone()[0] == password:
            return conn.execute(sqlalchemy.text(f"""SELECT attr_level FROM users WHERE username = '{username}'""")).fetchone()[0]
        else:
            return 0
