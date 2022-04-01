#
#   dboスキーマの表を、別のスキーマにバックアップする。
#
#   usage:
#           py copy_tables.py [スキーマ名]
#
#   ・引数にスキーマ名を指定した場合のみ、バックアップを実行する。
#   ・引数にスキーマ名を指定しない場合は、バックアップ対象の表の行数を一覧する。
#
#   ・データの保全には、当初、"DBの複製"を考えていたが、
#   　課金量が増えそうなので、"表の複製"をすることにした。
#   ・複製先は、別の"スキーマ"
#
#    利用前提:
#    ・環境変数"AzureSQLConnectionString"にDB接続情報が設定されていること
#       DRIVER={ODBC Driver 17 for SQL Server};
#       SERVER=tgpower-db-server.database.windows.net;DATABASE=tgpower-db;
#       UID={db login};PWD={login password}
#
# @author kazuhiko@jomura.net
# @version 2022.02.16

import sys
import os
# import time
import pyodbc


try:
    # newSchemaName = time.strftime('%Y%m%d', time.localtime())
    newSchemaName = None
    if len(sys.argv) > 1:
        newSchemaName = sys.argv[1]
        print("NEW_SCHEMA_NAME: " + newSchemaName)

    cnn = pyodbc.connect(os.environ['AzureSQLConnectionString'])
    cur = cnn.cursor()

    if newSchemaName is not None:
        queryStr = f"CREATE SCHEMA [{newSchemaName}] AUTHORIZATION dbo"
        print(queryStr)
        cur.execute(queryStr)
        cnn.commit()

    queryStr = "select name \
        from sys.objects \
        where type = 'U' \
        and schema_id = schema_id('dbo') \
        order by create_date"
    cur.execute(queryStr)

    for tablename in [row[0] for row in cur.fetchall()]:
        queryStr = f"SELECT count(*) FROM [dbo].[{tablename}]"
        cur.execute(queryStr)
        row = cur.fetchone()
        if row:
            print("%s : %d" % (tablename, row[0]))

        if newSchemaName is not None:
            queryStr = f"SELECT * INTO [{newSchemaName}]"\
                f".[{tablename}] FROM [dbo].[{tablename}]"
            print(queryStr)
            cur.execute(queryStr)

    cnn.commit()

    cur.close()
    cnn.close()

except BaseException as e:
    print(e)
    raise
