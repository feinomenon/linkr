from flask import Flask, render_template, request, redirect, url_for

import random
import sqlite3

app = Flask(__name__)
app.debug = True
app.reload = True

# TODO: Turn this into a database
url_dict = {}

def transform(length=10):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz')
        for x in range(length)])

def store_url(orig_url, short_url, db):
    # TODO: This will take an actual db
    db[short_url] = orig_url

def retrieve_url(short_url, db):
    return db[short_url]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<short_url>')  #Dynamic URL
def retrieve(short_url):
    orig_url = retrieve_url(short_url, url_dict)
    return redirect(orig_url)

@app.route('/forms', methods=['POST'])
def process_form():
    orig_url = request.form['url']
    if not orig_url.startswith('http://'):
        orig_url = ''.join(('http://', orig_url))
    new_url = transform()
    store_url(orig_url, new_url, url_dict)
    print(url_dict)
    return new_url


if __name__ == '__main__':
    app.run('localhost', 5000)
