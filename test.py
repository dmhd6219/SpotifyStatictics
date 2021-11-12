import json
from pprint import pprint

import requests

with open('./.spotify_caches/a5831539-b16a-4c37-a5d2-a5b0b90676d6') as file:
    token = json.load(file)['access_token']

sp_dc = 'AQBQoHtDHBPp0oST7oiof6Njb-3aDqnNeHRlGi3jTF7EeGKT0uypGnwUklatlhtv5hG5PnDv5Xu49arRkBUHC7f_j1pJoytYjzrTo-UojX5awA'

hd = ('Connection', 'keep-alive'), ('Sec-Ch-Ua', '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"'), ('Sec-Ch-Ua-Mobile', '?0'), ('Sec-Ch-Ua-Platform', '"Windows"'), ('Upgrade-Insecure-Requests', '1'), ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('Purpose', 'prefetch'), ('Sec-Fetch-Site', 'none'), ('Sec-Fetch-Mode', 'navigate'), ('Sec-Fetch-User', '?1'), ('Sec-Fetch-Dest', 'document'), ('Accept-Encoding', 'gzip, deflate, br'), ('Accept-Language', 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7')

headers = {'Authorization': f'Bearer {token}'}
for i in hd:
    headers[i[0]] = i[1]



pprint(requests.get('https://accounts.spotify.com/login/password', data={
    'username':'svyatoslavsvyatkin@yandex.ru',
    'password':'Qweasd228!'
}).text)

pprint(requests.get('https://guc-spclient.spotify.com/presence-view/v1/buddylist',
    headers= headers
    ).json())

print('--------')
pprint(
    requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player',
                 headers={
                     'Cookie' : f'sp_dc={sp_dc}'
                 }).json()
)