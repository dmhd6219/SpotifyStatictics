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


@app.route('/')
@spotify_login_required
def index(spotify: Spotify):
    account = spotify.me()

    pprint(account)
    return render_template('index.html', data=account)


@app.route('/stats/tracks/<term>')
@spotify_login_required
def tracks_stats(spotify: Spotify, term):
    if term not in ('short', 'medium', 'long'):
        abort(404)

    tracks = []
    for i in range(5):
        for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range=term + '_term')['items']:
            tracks.append(track)

    return render_template('tracks_test.html', data=tracks, term=term)


@app.route('/stats/artists/<term>')
@spotify_login_required
def artists_stats(spotify: Spotify, term):
    if term not in ('short', 'medium', 'long'):
        abort(404)

    artists = []
    for i in range(5):
        for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range=term + '_term')['items']:
            artists.append(artist)

    return render_template('artists.html', data=artists, term=term)


if __name__ == '__main__':
    app.run(threaded=True, port=8080)
