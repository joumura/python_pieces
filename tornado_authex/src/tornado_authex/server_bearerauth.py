"""
    tornadoを使ったBearer認証の実装例

    認証情報はDUKE LDAP。
    最初にログインAPI(/login)で、tokenを取得する必要がある。
    ログアウトAPI(/logout)が呼ばれるか、サーバ再起動すると、認証済みtokenは消える。

    RequestHandlerの対象メソッドに、@bearer_auth(api_auth) と書くと、Bearer認証が効く。
    引数で認証・認可判断処理を変更可能。

    TODO: 最終アクセス時刻を元に、不要なtokenを自動削除する仕組み。(timeout)

    @author kazuhiko@jomura.net
    @version 2022.03.29
"""
import os
import tornado.ioloop
import tornado.web
from tornado.options import options as toropt
import signal
from pathlib import Path
from logging import getLogger
from bearer_auth import LoginHandler, LogoutHandler
from handlers_bearerauth import JsonHandler


logger = getLogger(__name__)

accect_ctlc = False


class Application(tornado.web.Application):
    """classを定義すべきかどうかは微妙。
    インスタンス化するだけの方がシンプルかも。
    """
    def __init__(self):
        BASE_DIR = get_root_path()
        handlers = [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/json", JsonHandler),
        ]
        handlers = [("/tornado" + url, handler) for (url, handler) in handlers]
        settings = dict(
            static_path=os.path.join(BASE_DIR, "static"),
            template_path=os.path.join(BASE_DIR, "templates"),
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
