# Web APIの認証

## 標準化されている認証方式
- Basic (RFC 2617)
- Digest (RFC 2617)
- Bearer (RFC 6750)
    - ヘッダーのAuthorizationに埋め込む方法
    - リクエストボディーへ埋め込む方法（access_tokenパラメータ）
    - クエリーパラメーターとして渡す方法（access_tokenパラメータ）
- OAuth2.0 (RFC 6749)
    - 認可専用
- OpenID Connect (OpenID Connect Core 1.0)
    - 認証用
- APIキー認証
    - 簡単に盗まれる(∵clientがアクセス可能な場所にあるから)
    - 匿名・非認証 (∵誰でも認証を通過できる)
- One-time password : security token
    - 補助的・副次的


## 使われ方

### ログインAPIによる認証 (stateful)
- 最初にログインAPIを呼んで、tokenとCookieをもらい、
- 業務API要求時に、AuthorizationヘッダでBearer認証する。
- 最後にログアウトAPIを呼んで、認証情報を破棄する。

### コード化(BASE64)認証情報を要求毎に付与 (stateless)
- 業務API要求時に、AuthorizationヘッダでBasic認証する。
- Authorization: Basic {username:passwordをBase64エンコードしたASCII文字列}

### OpenID認証
- 基本的には、"ログインAPIによる認証"と同じ
- OpenIDプロバイダをtoken issuerとする
- 非認証時にOpenIDプロバイダへredirectする仕組み
