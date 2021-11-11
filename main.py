import os
from collections import defaultdict
from pprint import pprint

import flask_session
from dotenv import load_dotenv
from flask import Flask, redirect, abort, render_template

from spotipy import Spotify

from utils.spotify import spotify_login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
flask_session.Session(app)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

if __name__ == '__main__':
    app.run(threaded=True, port=8080)
