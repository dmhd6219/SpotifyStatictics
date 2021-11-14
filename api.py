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


def stats(spotify: Spotify, type_, term):
    if term not in ('long', 'medium', 'short'):
        return make_response(jsonify({'error': f'There are not "{term}" term. Try long, medium or short.'}), 404)

    if type_ == 'tracks':
        top_tracks = []
        for i in range(5):
            for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range=term + '_term')['items']:
                del track['available_markets']
                del track['album']['available_markets']
                top_tracks.append(track)
        return make_response(jsonify({'success': 'ok', 'data': top_tracks}), 200)

    if type_ == 'artists':
        top_artists = []
        for i in range(5):
            for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range='long_term')['items']:
                top_artists.append(artist)
        return make_response(jsonify({'success': 'ok', 'data': top_artists}), 200)

    return make_response(jsonify({'error': f'There no "{type_}" type. Try artists or tracks.'}))


def me(spotify: Spotify):
    data = spotify.me()

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)


def playback(spotify: Spotify):
    data = spotify.current_playback()

    if data is None or data.get('error'):
        return make_response(jsonify({'error': 'Track is not playing rn.'}), 404)

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)
