""" frontend thing """
from flask import Flask, render_template

frontend = Flask(__name__)

@frontend.route('/')
def index():
    return render_template('index.html', title="Dashboard")

@frontend.route('/incoming')
def incoming():
    return render_template('incoming.html', title="Incoming")