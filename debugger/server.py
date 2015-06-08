# all the imports
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify)

import jinja2

from collections import deque, defaultdict
import os
import json

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    os.path.join(os.getcwd(), "templates"),
])
app.jinja_load = my_loader


@app.route('/', methods=('GET',))
def index():
    q = request.args.get("q", "index")
    return render_template('{0}.html'.format(q))

current_states = defaultdict(lambda:deque())


@app.route('/push_state', methods=('POST', ))
def push_state():
    current_states[request.form.get("jobname", "default")].append(request.form.copy())
    return render_template('index.html')


@app.route('/get_current_state', methods=('GET',))
def get_current_state():
    jobname = request.args.get("jobname", "default")
    if len(current_states[jobname]):
        state = current_states[jobname].popleft()
    else:
        abort(404)
    return jsonify(state)

if __name__ == '__main__':
    app.run()
