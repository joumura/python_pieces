import functools
import secrets
import time
import tornado.web
import json
from tornado_authex.arth import adldap


def bearer_auth(auth):
    def decore(f):
        def _request_auth(handler):
            handler.set_status(401)
            handler.finish()
            return False

        @functools.wraps(f)
        def new_f(*args):
            handler = args[0]

            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None:
                return _request_auth(handler)
            if not auth_header.startswith('Bearer '):
                return _request_auth(handler)

            if (auth(auth_header[7:])):
                f(*args)
            else:
                _request_auth(handler)

        return new_f
    return decore


# スレッドセーフらしい
authtokens = {}


def api_auth(tokenstr):
    """認証および認可(2)"""
    if tokenstr in authtokens:
        # 最終アクセス時刻を更新する
        authtokens[tokenstr][1] = time.time()
        return True
    else:
        return False


class LoginHandler(tornado.web.RequestHandler):
    """ログインAPI"""
    def prepare(self):
        if self.request.headers['Content-Type'] == 'application/x-json':
            self.args = json.loads(self.request.body)

    def post(self):
        username = self.args["username"]
        password = self.args["password"]
        if self.is_member(username, password):
            # tokenを返す
            tokenstr = secrets.token_urlsafe(16)
            authtokens[tokenstr] = [username, time.time()]
            self.write(json.dumps({"authtoken": tokenstr}))
        else:
            # 認証エラー
            self.send_error(401)

    def is_member(self, username, password):
        """認証および認可(1)"""
        # return username == "user" and password == "pass"
        entry = adldap.authenticate(username, password)
        return adldap.in_authorized_group(entry, ['G2-171500000s'])


class LogoutHandler(tornado.web.RequestHandler):
    """ログアウトAPI"""
    def get(self):
        auth_header = self.request.headers['Authorization']
        authtokens.pop(auth_header[7:])
