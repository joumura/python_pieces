azure-sql-util
==========

　Azure SQLを利用する際に、必要になった運用ツール達。


azure_sql_util
==========
　Azure SQLを使う際に、以下の手続きを助けるGUI。
1. ログインパスワードの変更
2. (管理者用) ログイン・ユーザの追加
3. (管理者用) ログイン・ユーザの削除

Usage
-----

　以下のコマンドでGUIが起動する。
```
py -m azure_sql_util
```
　本当に使うなら、pythonが導入されていない環境のために、pyinstallerでexe化するのがよいだろう。

----

copy_tables
==========
　Azure SQLのデータをバックアップしたい場合に、別DBを作ると課金額が増える。ので、別スキーマに複製するためのツール。

Usage
-----

　以下のコマンドで、バックアップ対象の表と行数が一覧できる。
```
py -m azure_sql_util.copy_table
```
　以下のコマンドで、{スキーマ名}に表を複製する。
```
py -m azure_sql_util.copy_table {スキーマ名}
```
