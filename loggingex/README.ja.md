loggingex
==========

　pythonライブラリloggingの拡張.  
　非常駐なpythonバッチのロギングに対して、
標準のRotatingFileHandlerとかTimedRotatingFileHandlerの仕様が
気に入らなかったので作成。  
　本体は、handlers.pyのMyTimedRotatingFileHandlerだけ。

- TimedRotatingFileHandlerと異なり、非常駐プロセスにも対応している。
    - 例えば、when='D'とすると、ログファイル名に日付が入り、ログが日毎に切り替わる。
        - 分割単位は、Y, M, D, H, MI が指定可能。
- ログファイル名は、指定された拡張子を維持する。
- 古いログファイルを削除する機能は無い。


Usage
-----

```ini
[handler_file]
class=loggingex.handlers.MyTimedRotatingFileHandler
args=('myapp.log', 'd', 'utf-8')
```

Demo
-----

```
py -m loggingex
```
