import sqlalchemy

def get_all_usr(conn)->list:
    return conn.execute(sqlalchemy.text("""SELECT username, attr_level FROM users""")).fetchall()
