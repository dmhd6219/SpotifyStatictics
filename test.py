import json
from pprint import pprint

import requests

with open('./.spotify_caches/6984d269-db9c-4c7f-bc28-cce42c3c45b8') as file:
    token1 = json.load(file)['access_token']

token2 = 'AQBk1-6S_Xu4n5gfmumJfh2XvjIriSPFUFUdW7DmCK-r9HTlS_eHEErkrS0EpQcfb2qjBF6JaulAJZVZ92bAKS3VtK1l4bx69BandzYWRPmZ3i8KNGSZQG5fiDsaebsVyZgZ25WScK-g5vsgVvMXsdaBTuoJW11-mlZbSxI0fYyn7ppXOBVq9PwUSVhQFgrhI-bkaRRPJO7KJ-_QhN8LRGltSvlBZIE00nRc9jR6B52guF4_XSngD0nrKhptWN2Etwp4kX8msZmw-E9fwNKmd67Ws5ohnLp9T2F-lggGxEI3h1CCnluDKOV5zxHT8wmilAE31esa9vN7KFNHrijE36XMGpKEAp3b6e6olVzRVMX1D8A7quy0C1Bq_IZxmuR3GQSU5ZyOwzueyuHP-y3mCk19i5qDQpg0sB2ZC-Wt9xCBDievywba1QIuPelHQ6Hcn4wNuOqXrjknfa18J_mXwSFaMh9pzsl5GMoxoD7TQjsLSF-4J0oY3L3tdBB0eBzIV-rIz8J9wPaZ-tWo_HkKvQvZLaLg8kM_Ny35VKUJQeW433MB6exG0I1Z8m4lTFmSQRbcvypYWcCQUWg8V9nQwzK48O1nX33uxf72492FAZS-rFZZS507YQkoUtuRVMQfePxK4h696SgNP5fS8vKWW7SDjkXbIQrLtqLc1wEfrUo8HWvTUp4XSg'


for token in (token1, token2):
    pprint(requests.get('https://api.spotify.com/v1/me', headers={
    'Authorization' : f'Bearer {token}'}).json())
    print('.................')