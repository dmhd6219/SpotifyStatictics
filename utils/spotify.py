import json
import os
import uuid

import requests
import spotipy
from flask import session, request, redirect

import api
from data import db_session
from data.users import User

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)
    print(f'Created spotify cache folder : {caches_folder}')

SCOPE = 'user-top-read user-read-playback-position user-read-private user-read-email ' \
        'playlist-read-private user-library-read user-library-modify playlist-read-collaborative ' \
        'playlist-modify-public playlist-modify-private ugc-image-upload user-follow-read ' \
        'user-follow-modify user-read-playback-state user-modify-playback-state ' \
        'user-read-currently-playing user-read-recently-played streaming'


def session_cache_path():
    return caches_folder + session.get('uuid')


def spotify_login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('uuid'):
            # Step 1. Visitor is unknown, give random ID
            print('# Step 1. Visitor is unknown, give random ID')
            session['new'] = True
            session['uuid'] = str(uuid.uuid4())

        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=SCOPE,
            cache_handler=cache_handler,
            show_dialog=True)

        # db_sess = db_session.create_session()
        # user = db_sess.query(User).get(current_user.id)

        if request.args.get("code"):
            # Step 3. Being redirected from Spotify auth page
            print('# Step 3. Being redirected from Spotify auth page')
            token = request.args.get("code")

            token = auth_manager.get_access_token(token)['access_token']

            if session.get('new'):
                spotify = spotipy.Spotify(auth_manager=auth_manager)

                account = spotify.me()
                email = account['email']

                # creating user in db

                user = User()
                user.email = email
                user.spotify_id = account['id']
                user.spotify_token = token

                user.favorite_track = api.stats(spotify, 'tracks', 'long').json['data'][0]['id']
                user.favorite_artist = api.stats(spotify, 'artists', 'long').json['data'][0]['id']

                db_sess = db_session.create_session()
                db_sess.add(user)
                db_sess.commit()

            return redirect('/')

        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            # Step 2. Redirect to spotify auth page when no token
            print('# Step 2. Redirect to spotify auth page when no token')
            auth_url = auth_manager.get_authorize_url()
            return redirect(auth_url)

        # Step 4. Signed in, display data
        spotify = spotipy.Spotify(auth_manager=auth_manager)

        # if not user.spotify_id or user.spotify_id != spotify.current_user()['id']:
        # user.spotify_id = spotify.current_user()['id']
        # db_sess.commit()

        if args:
            return func(*args, **kwargs)

        return func(*args, **kwargs, spotify=spotify)

    wrapper.__name__ = func.__name__
    return wrapper


class TokenSpotify():
    def __init__(self, token):
        self.token = token

    def get(self, method, **kwargs):
        return requests.get(f'https://api.spotify.com/v1/{method}', headers={
            'Authorization': f'Bearer {self.token}'}, data=kwargs).json()

    def me(self):
        return self.get('me')

    def current_playback(self):
        return self.get('me/player')

    def top(self, type_, **kwargs):
        return self.get(f'me/top/{type_}', **kwargs)

    def track(self, id_):
        return self.get(f'tracks/{id_}')

    def artist(self, id_):
        return self.get(f'artists/{id_}')
