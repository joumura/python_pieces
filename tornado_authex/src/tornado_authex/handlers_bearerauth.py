import json
import tornado.web
from bearer_auth import bearer_auth, api_auth


class JsonHandler(tornado.web.RequestHandler):
    """json応答のサンプル"""
    @bearer_auth(api_auth)
    def get(self):
        self.set_header("Content-Type", 'application/json')
        self.write(json.dumps({"jsontext": "Hello world"}))
