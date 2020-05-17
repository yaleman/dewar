""" frontend thing """
from loguru import logger
from flask import Flask, render_template, current_app

frontend = Flask(__name__)

@frontend.route('/')
def index():
    """ dashboard/home page """
    return render_template('index.html', title="Dashboard")

@frontend.route('/incoming')
def incoming():
    """ incoming parser """
    dewar = current_app.config.get('dewar')
    file_list = dewar.get_incoming_files()
    return render_template('incoming.html',
                           title="Incoming",
                           knowngood=file_list.get('knowngood'),
                           other=file_list.get('other'),
                           )

@frontend.route('/incoming/process/<bucket>/<filename>')
def process_file(bucket, filename):
    """ process a file """
    #dewar = current_app.config.get('dewar')

    return render_template('process_file.html',
                           title="Processing file...",
                           filename=f"{bucket}/{filename}"
                           )
