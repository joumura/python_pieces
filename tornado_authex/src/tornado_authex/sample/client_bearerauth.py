from requests import Session
import json
from tornado_authex.crypt import aes

# ログインAPI
sess = Session()
headers = {'Content-Type': 'application/x-json'}
post_data = {"username": "k-jyoumura",
             "password": aes("tgpower").decrypt_str('Y2e5CvkfZSRgcNpNrkIQLg==')}
res = sess.post('http://localhost:8888/tornado/login',
                data=json.dumps(post_data), headers=headers)
print(res.text)
authtoken = 'Bearer ' + json.loads(res.text)['authtoken']

# 業務API
headers = {'Content-Type': 'application/x-json',
           'Authorization': authtoken}
res = sess.get('http://localhost:8888/tornado/json', headers=headers)
print(res.status_code)
print(res.text)

# ログアウトAPI
headers = {'Content-Type': 'application/x-json',
           'Authorization': authtoken}
res = sess.get('http://localhost:8888/tornado/logout', headers=headers)
print(res.status_code)
print(res.text)

# 業務API・失効
headers = {'Content-Type': 'application/x-json',
           'Authorization': authtoken}
res = sess.get('http://localhost:8888/tornado/json', headers=headers)
print(res.status_code)
print(res.text)
