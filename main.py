import os
from collections import defaultdict
from pprint import pprint

import flask_session
from dotenv import load_dotenv
from flask import Flask, redirect, abort, render_template

from spotipy import Spotify

import api
from utils.spotify import spotify_login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
flask_session.Session(app)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


@app.route('/')
@spotify_login_required
def index(spotify: Spotify):
    return 'ok'


@app.route('/debug')
@spotify_login_required
def debug(spotify: Spotify):
    pprint(api.stats(spotify, 'tracks', 'long').json['data'])
    return 'debugging........'


@app.route('/me')
@spotify_login_required
def me(spotify: Spotify):
    data = {
        'profile': api.me(spotify).json['data'],
        'playback' : api.playback(spotify).json['data'],
        'top_track' : api.stats(spotify, 'tracks', 'long').json['data'][0],
        'top_artist': api.stats(spotify, 'artists', 'long').json['data'][0],

    }
    return render_template('profile.html', **data)


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    app.run(threaded=True, port=8080, debug=True)
