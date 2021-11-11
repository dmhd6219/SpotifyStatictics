import flask
from flask import make_response, jsonify
from spotipy import Spotify

from utils.spotify import spotify_login_required

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


def stats(spotify: Spotify, category, term):
    if category not in ('artists', 'tracks'):
        return make_response(jsonify({'error': f'Cant find statistics for "{category}". Use artists or tracks.'}), 404)
    if term not in ('short', 'medium', 'long'):
        return make_response(jsonify({'error': f'Cant find statistics for "{term}" term. Use short, medium or long.'}),
                             404)

    if category == 'tracks':
        tracks = []
        for i in range(5):
            for track in spotify.current_user_top_tracks(limit=20, offset=20 * i, time_range=term + '_term')['items']:
                del track['available_markets']
                del track['album']['available_markets']
                tracks.append(track)
        return make_response(jsonify({'success': 'OK', 'data': tracks}), 200)

    if category == 'artists':
        artists = []
        for i in range(5):
            for artist in spotify.current_user_top_artists(limit=20, offset=20 * i, time_range=term + '_term')['items']:
                artists.append(artist)
        return make_response(jsonify({'success': 'OK', 'data': artists}), 200)

    return make_response(jsonify({'error': 'Unknown error'}), 404)


def me(spotify: Spotify):
    data = spotify.me()

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)


def playback(spotify: Spotify):
    data = spotify.current_playback()

    del data['item']['album']['available_markets']
    del data['item']['available_markets']

    return make_response(jsonify({'success': 'OK', 'data': data}), 200)
