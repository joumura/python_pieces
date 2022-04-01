# 注意点
1. DUKE LDAP認証で
    - メールアドレスで認証する場合 ⇒ 事前設定として"LDAP接続情報"が必要
    - DUKE IDで認証する場合 ⇒ 事前設定は不要(∵入力値でLDAP接続を試みるため)
2. "LDAP接続情報"には統合IDパスワードが含まれる。
    - パスワードの暗号化をサンプル実装している。 必要なら
        - ライブラリ: crypt.py
        - 利用箇所: arth.py


# Form認証
- server.py

# BASIC認証
- 要求都度、LDAPに問合せる
- server_basicauth.py
- client_basicauth.py

# Bearer(token)認証
- 最初に認証し、tokenを持ちまわして認可する
- server_bearerauth.py
- client_bearerauth.py
