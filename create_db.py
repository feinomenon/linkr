import sqlite3

con = sqlite3.connect('urls.db')
c = con.cursor()
c.execute('''
    CREATE TABLE if not exists urlmap
    (short_url varchar unique,
    orig_url varchar)
    ''')
con.commit()
