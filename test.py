import json
from pprint import pprint

import requests

sp_dc = 'AQBQoHtDHBPp0oST7oiof6Njb-3aDqnNeHRlGi3jTF7EeGKT0uypGnwUklatlhtv5hG5PnDv5Xu49arRkBUHC7f_j1pJoytYjzrTo-UojX5awA'

tk = 'AQBEdLRMa4TZJJex7qU9_4zxJhwO6S6hvqzVPnIkrdKGT-ecb-xc_ZctLB1cS2lxCrFcHmYanPgxcmPZoy1ngfACTK0fk3Eg-Y94T4DtC-f0PHSlA03CFMBVxYYOULwMR8_FyTbvR9Hog5h0whHxuwGuVcYTh7CpAc2fUA6H1DDXU1KOn7REVzSCHqBZ0oG1OroqfpgARFeiDmxt3-ciHFPzmmIm5cpcOC4Uhs7suhbegh9TV-ZMOuT1ZRduPoC1XMRsauByeDRsv0kEe-7rnq2ebNkfBkexYKjlDd4vJ8SlzknWO3Im9HrZ6BkY6Oyk_e5qh_Yv7nrX4y2qPRBZ4odlDpHvXOl61SvOux9BAPIO7MkM7X9RpCbei-daXubvtSjJ31AfLt_9HoFrFeww-TqaPmmDOsqra2Y1EaAu6L5kt8owY94g4-DwYQFupfS9A9oDi145ol0BwsAvFc3ohXsmlJoX37SISobX5FdoPZB-hBZ37h5bdOv61PwNcq4bLMp6Au7kp-fdG2H5uSNqkQTTI1YU2QFHOHqGdAGW-O4QQ9i9HFWtHaOvHNtL8TPWFh-EFD06YBjaxAFhjx1oak3Ej9QdoqyHNApjjLcXg3QYiYDjJYza09kclXJu3XnnhWiPLKiO3blse9h8gglURcUOBOPc8EX2LUHK4EWpSee6BXviuyxECg'


def get_spotify_token(sp_dc):
    response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player',
                            headers={
                                'Cookie': f'sp_dc={sp_dc}'
                            }).json()

    pprint(response)

    return response['accessToken']


def get_token(code):
    response = requests.get(f'https://api.spotify.com/v1/token',
                            data={'code': code})

    return response.text


class SpotifyToken:
    def __init__(self, sp_dc):
        self.token = get_spotify_token(sp_dc)

        pprint(self.token)

    def get(self, method, **kwargs):
        response = requests.get(f'https://api.spotify.com/v1/{method}',
                                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'},
                                data=kwargs)

        return response.json()

    def top(self, type_, term):
        if term not in ('long', 'medium', 'short') or type_ not in ('tracks', 'artists'):
            return None

        response_json = self.get(f'top/{type_}', time_range=f'{term}_term')
        return response_json

    def current_playback(self):
        response_json = self.get('player/currently-playing')
        return response_json

    def me(self):
        response_json = self.get('me')
        return response_json

    def track(self, id_):
        response_json = self.get(f'tracks/{id_}')
        return response_json

    def artist(self, id_):
        response_json = self.get(f'artists/{id_}')
        return response_json


pprint(get_token(tk))