import datetime
from pprint import pprint

import flask
from flask import make_response, jsonify
from spotipy import Spotify

import utils.spotify
from data import db_session
from data.users import User
from utils.spotify import spotify_login_required

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


def stats(spotify: Spotify):
    top_tracks_long = []
    for i in range(5):
        for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range='long_term')['items']:
            del track['available_markets']
            del track['album']['available_markets']
            top_tracks_long.append(track)
    ids_top_tracks_long = utils.spotify.top_ids(top_tracks_long)

    top_tracks_medium = []
    for i in range(5):
        for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range='medium_term')['items']:
            del track['available_markets']
            del track['album']['available_markets']
            top_tracks_medium.append(track)
    ids_top_tracks_medium = utils.spotify.top_ids(top_tracks_medium)

    top_tracks_short = []
    for i in range(5):
        for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range='short_term')['items']:
            del track['available_markets']
            del track['album']['available_markets']
            top_tracks_short.append(track)
    ids_top_tracks_short = utils.spotify.top_ids(top_tracks_short)

    top_artists_long = []
    for i in range(5):
        for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range='long_term')['items']:
            top_artists_long.append(artist)
    ids_top_artists_long = utils.spotify.top_ids(top_artists_long)

    top_artists_medium = []
    for i in range(5):
        for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range='medium_term')['items']:
            top_artists_medium.append(artist)
    ids_top_artists_medium = utils.spotify.top_ids(top_artists_medium)

    top_artists_short = []
    for i in range(5):
        for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range='short_term')['items']:
            top_artists_short.append(artist)
    ids_top_artists_short = utils.spotify.top_ids(top_artists_short)

    db_sess = db_session.create_session()
    email = me(spotify).json['data']['email']
    user = db_sess.query(User).filter(User.email == email).first()

    user.top_tracks_long = ids_top_tracks_long
    user.top_tracks_medium = ids_top_tracks_medium
    user.top_tracks_short = ids_top_tracks_short
    user.top_artists_long = ids_top_artists_long
    user.top_artists_medium = ids_top_artists_medium
    user.top_artists_short = ids_top_artists_short

    user.top_data = datetime.datetime.now()

    db_sess.commit()

    return make_response(jsonify({'success': 'ok', 'data': {
        'artists': {'long': top_artists_long, 'medium': top_artists_medium, 'short': top_artists_short},
        'tracks': {'long': top_tracks_long, 'medium': top_tracks_medium, 'short': top_tracks_short}
    }}), 200)


def me(spotify: Spotify):
    data = spotify.me()

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)


def playback(spotify: Spotify):
    data = spotify.current_playback()

    if data is None or data.get('error'):
        return make_response(jsonify({'error': 'Track is not playing rn.'}), 404)

    pprint(data)

    del data['item']['album']['available_markets']
    del data['item']['available_markets']

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)
