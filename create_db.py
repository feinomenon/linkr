import sqlite3

def connect_db():
    return sqlite3.connect('urls.db')

def init_db():
    con = connect_db()
    c = con.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urlmap
        (short_url varchar unique,
        orig_url varchar)
        ''')
    con.commit()
    con.close()
