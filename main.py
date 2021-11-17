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


@app.route('/debug')
@spotify_login_required
def debug(spotify: Spotify):
    pprint(api.playback(spotify).json['data'])
    return ', '.join(os.listdir("../")) + f'<a href="/me">CLICK HERE</a><br>'


@app.route('/')
@spotify_login_required
def index(spotify: Spotify):
    return f'<a href="/me">{spotify.me()["display_name"]}</a>'


@app.route('/me')
@spotify_login_required
def me(spotify: Spotify):
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.email == api.me(spotify).json['data']['email']).first()
    if user.link:
        return redirect(f'/profile/{user.link}')
    if not user.link:
        return redirect(f'/profile/{user.spotify_id}')

    return render_template('profile.html')


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
        if user.link:
            return redirect(f'/profile/{user.link}')

    user_spotify = Spotify(auth_manager=user.spotify_auth_manager)

    data = {'me': api.me(spotify).json['data'],
            'playback': api.playback(user_spotify).json.get('data'),
            'profile': api.me(user_spotify).json['data'],
            'top_genres': api.stats(user_spotify, 'genres', 'long').json['data'][:6],
            'status': user.status,

            }

    if user.favorite_track:
        data['top_track'] = user_spotify.track(user.favorite_track)

    if user.favorite_artist:
        data['top_artist'] = user_spotify.artist(user.favorite_artist)

    return render_template('profile.html', **data)


@app.route('/stats/<id>/<type>/<term>')
@spotify_login_required
def stats(spotify: Spotify, id, type, term):
    if type not in ('tracks', 'artists'):
        abort(404)
    if term not in ('short', 'medium', 'long'):
        abort(404)

    db_sess = db_session.create_session()

    query = db_sess.query(User).filter(User.link == id)
    user = query.first()
    if not user:
        query = db_sess.query(User).filter(User.spotify_id == id)
        user = query.first()
        if not user:
            abort(404)
        if user.link:
            return redirect(f'/profile/{user.link}')

    user_spotify = Spotify(auth_manager=user.spotify_auth_manager)

    data = {'me': api.me(spotify).json['data'],
            'playback': api.playback(user_spotify).json.get('data'),
            'profile': api.me(user_spotify).json['data'],
            'data': api.stats(user_spotify, type, term).json['data'],
            'term': term
            }
    if type == 'artists':
        return render_template('artists.html', **data)
    if type == 'tracks':
        return render_template('tracks.html', **data)


@app.route('/profiles')
@spotify_login_required
def profiles(spotify: Spotify):
    db_sess = db_session.create_session()

    query = db_sess.query(User).all()

    data = []

    for user in query:
        user_spotify = Spotify(auth_manager=user.spotify_auth_manager)

        data.append(user_spotify.me())

    return render_template('profiles.html', data=data, me=spotify.me())


if __name__ == '__main__':
    db_session.global_init("./db/data.sqlite")

    app.register_blueprint(api.blueprint)
    app.run(threaded=True, port=8080, debug=True)
