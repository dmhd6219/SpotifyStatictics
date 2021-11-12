import os
from collections import defaultdict
from pprint import pprint

import flask_session
from dotenv import load_dotenv
from flask import Flask, redirect, abort, render_template, request

from spotipy import Spotify

from data import db_session

import api
from data.users import User
from utils.spotify import spotify_login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SQLALCHEMY_DATABASE_URI'] = './db/data.sqlite'
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
    pprint(request.headers)
    return 'debugging........'


@app.route('/me')
@spotify_login_required
def me(spotify: Spotify):
    data = {
        'profile': api.me(spotify).json['data'],

    }

    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.email == data['profile']['email']).first()
    if user.link:
        return redirect(f'/profile/{user.link}')
    if not user.link:
        return redirect(f'/profile/{user.spotify_id}')

    data['top_track'] = spotify.track(user.favorite_track)
    data['top_artist'] = spotify.artist(user.favorite_artist)
    data['playback'] = api.playback(spotify).json.get('data'),

    return render_template('profile.html', **data)


@app.route('/profile/<id>')
@spotify_login_required
def profile(spotify: Spotify, id):
    db_sess = db_session.create_session()

    query = db_sess.query(User).filter(User.link == id)
    user = query.first()
    if not user:
        query = db_sess.query(User).filter(User.spotify_id == id)
        user = query.first()
    if not user:
        abort(404)

    data = {'profile': api.me(spotify).json['data'], 'playback': api.playback(spotify).json.get('data'),
            'top_track': spotify.track(user.favorite_track), 'top_artist': spotify.artist(user.favorite_artist)}

    return render_template('profile.html', **data)



if __name__ == '__main__':
    db_session.global_init("./db/data.sqlite")

    app.register_blueprint(api.blueprint)
    app.run(threaded=True, port=8080, debug=True)
