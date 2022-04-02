import requests
from requests.auth import HTTPBasicAuth
from tornado_authex.crypt import aes

res = requests.get(
    'http://localhost:8888/tornado/json',
    auth=HTTPBasicAuth(
        "k-jyoumura",
        aes("tgpower").decrypt_str('Y2e5CvkfZSRgcNpNrkIQLg==')))
print(res.status_code)
print(res.text)
