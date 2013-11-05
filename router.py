from flask import Flask, g, redirect, render_template, request, url_for
from create_db import connect_db, init_db
from contextlib import closing
import random
import sqlite3

# TODO: move config to separate file
app = Flask(__name__)
app.debug = True
app.reload = True
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def retrieve_url(new_url, db):
    query = 'SELECT orig_url FROM urlmap WHERE short_url=:url'
    c = db.cursor()
    c.execute(query, {'url': new_url})
    result = c.fetchone()[0]
    # print("RESULT:", result)
    queryall = 'SELECT * FROM urlmap'
    c.execute(queryall)
    data = c.fetchall()
    print("DATA:", data)
    return result

def store_url(orig_url, short_url, db):
    # TODO: This will take an actual db
    # db[short_url] = orig_url
    db.cursor().execute("INSERT INTO urlmap VALUES (?, ?)",
                        (short_url, orig_url))
    db.commit()

def transform(length=10):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
        for _ in range(length))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<short_url>')  #Dynamic URL
def retrieve(short_url):
    orig_url = retrieve_url(short_url, g.db)
    return redirect(orig_url)

@app.route('/forms', methods=['POST'])
def process_form():
    orig_url = request.form['url']
    if not orig_url.startswith('http'):
        orig_url = ''.join(('http://', orig_url))

    new_url = transform()
    store_url(orig_url, new_url, g.db)
    # print(url_dict)
    return new_url

if __name__ == '__main__':
    init_db()
    app.run('localhost', 5000)
