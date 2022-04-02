import os
import tornado.ioloop
import tornado.web
import signal
from tornado.options import options as toropt
from pathlib import Path
import json
from tornado_authex.arth import adldap
from logging import getLogger

logger = getLogger(__name__)

accect_ctlc = False


class BaseHandler(tornado.web.RequestHandler):
    """
        基底ハンドラ
        ログイン情報の制御
    """
    cookie_username = "username"

    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
        if not username:
            return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        self.set_secure_cookie(
            self.cookie_username,
            tornado.escape.utf8(username),
            expires_days=0.01)

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class IndexHandler(BaseHandler):
    """
        ルートページ
        @tornado.web.authenticated で認証追加
    """
    @tornado.web.authenticated
    def get(self):
        # for h in self._headers:
        #     logger.info(h + ": " + self._headers[h])
        user = self.get_current_user().decode()
        self.write("Hello, <b>%s</b> <br>"
                   " <a href=\"/tornado/auth/logout\">Logout</a>" % user)


class AuthLoginHandler(BaseHandler):
    """ログインページ"""
    def get(self):
        next = self.get_argument("next")
        if next:
            alert = "ログインが必要です。"
        self.render("login.html", next=next, alert=alert)

    def post(self):
        # csrf token check
        self.check_xsrf_cookie()
        username = self.get_argument("username")
        password = self.get_argument("password")
        if self.is_member(username, password):
            # 認証OKなら、セッションにusernameをセット
            self.set_current_user(username)
            # ログイン前に要求されたページに遷移
            self.redirect(self.get_argument("next"))
        else:
            # 認証エラー
            self.send_error(401)

    def is_member(self, username, password):
        """認証および認可"""
        # return username == "user" and password == "pass"
        entry = adldap.authenticate(username, password)
        return adldap.in_authorized_group(entry, ['G2-171500000s'])


class AuthLogoutHandler(BaseHandler):
    """ログアウトページ"""
    def get(self):
        # セッションのusernameをクリア
        self.clear_current_user()
        self.redirect('/tornado/')


class HelloHandler(BaseHandler):
    """html応答のサンプル"""
    @tornado.web.authenticated
    def get(self):
        self.render("hello.html", username=self.get_current_user().decode())


class JsonHandler(BaseHandler):
    """json応答のサンプル"""
    @tornado.web.authenticated
    def get(self):
        self.set_header("Content-Type", 'application/json')
        self.write(json.dumps({"jsontext": "Hello world"}))


class Application(tornado.web.Application):
    """classを定義すべきかどうかは微妙。
    インスタンス化するだけの方がシンプルかも。
    """
    def __init__(self):
        BASE_DIR = get_root_path()
        handlers = [
            (r"/", IndexHandler),
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            (r"/hello", HelloHandler),
            (r"/json", JsonHandler),
        ]
        handlers = [("/tornado" + url, handler) for (url, handler) in handlers]
        settings = dict(
            cookie_secret='secret_key',
            static_path=os.path.join(BASE_DIR, "static"),
            template_path=os.path.join(BASE_DIR, "templates"),
            login_url="/tornado/auth/login",
            xsrf_cookies=True,
            autoescape="xhtml_escape",
            # コード変更したら自動でサービス再起動
            # debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def get_root_path():
    return Path(__file__).resolve().parents[0]


def signal_handler(signum, frame):
    global accect_ctlc
    accect_ctlc = True


def try_exit():
    """Ctrl+Cでプロセス停止する"""
    global accect_ctlc
    if accect_ctlc:
        tornado.ioloop.IOLoop.instance().stop()


def main():
    toropt.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    app = Application()
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


# class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
#                                tornado.auth.GoogleOAuth2Mixin):
#     async def get(self):
#         if self.get_argument('code', False):
#             user = await self.get_authenticated_user(
#                 redirect_uri='http://your.site.com/auth/google',
#                 code=self.get_argument('code'))
#             # Save the user with e.g. set_secure_cookie
#         else:
#             await self.authorize_redirect(
#                 redirect_uri='http://your.site.com/auth/google',
#                 client_id=self.settings['google_oauth']['key'],
#                 scope=['profile', 'email'],
#                 response_type='code',
#                 extra_params={'approval_prompt': 'auto'})


# class FacebookGraphLoginHandler(tornado.web.RequestHandler,
#                                 tornado.auth.FacebookGraphMixin):
#   async def get(self):
#       if self.get_argument("code", False):
#           user = await self.get_authenticated_user(
#               redirect_uri='/auth/facebookgraph/',
#               client_id=self.settings["facebook_api_key"],
#               client_secret=self.settings["facebook_secret"],
#               code=self.get_argument("code"))
#           # Save the user with e.g. set_secure_cookie
#       else:
#           self.authorize_redirect(
#               redirect_uri='/auth/facebookgraph/',
#               client_id=self.settings["facebook_api_key"],
#               extra_params={"scope": "read_stream,offline_access"})


# class TwitterLoginHandler(tornado.web.RequestHandler,
#                           tornado.auth.TwitterMixin):
#     async def get(self):
#         if self.get_argument("oauth_token", None):
#             user = await self.get_authenticated_user()
#             # Save the user using e.g. set_secure_cookie()
#         else:
#             await self.authorize_redirect()
