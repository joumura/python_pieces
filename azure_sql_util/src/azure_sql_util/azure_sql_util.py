"""
   Azure SQL Util?

   運用補助ツール

   @auther kazuhiko@jomura.net
   @version 2022.04.01 refactor
   @version 2022.02.24 create
"""
import PySimpleGUI as sg
import pyodbc
import os
import datetime
import pickle


class azure_sql_util():

    def __init__(self):
        self.DEBUG = False
        self.CONNECT_STRING = "DRIVER={{ODBC Driver 17 for SQL Server}};"\
            "SERVER={servername};DATABASE={dbname};"\
            "UID={loginname};PWD={pw}"

        sg.theme('DarkBlue11')

        # restore configs
        oVals = {}
        if os.path.isfile('settings.pkl'):
            with open('settings.pkl', 'rb') as f:
                oVals = pickle.load(f)

        layout = [
            [sg.MenuBar([['ファイル', ['値を保存して終了']],
                        ['ヘルプ', ['必要ですか？']]], key='myMenu')],
            [sg.Text('SQL Server名:', size=(14, 1)),
                sg.InputText(
                    oVals.get('servername',
                              'tgpower-db-server.database.windows.net'),
                    key='servername', size=(50, 1))],
            [sg.Text('database名:', size=(14, 1)),
                sg.InputText(
                    oVals.get('dbname', 'tgpower-db'),
                    key='dbname', size=(50, 1))],
            [sg.Text('接続ログイン名:', size=(14, 1)),
                sg.InputText(
                    oVals.get('loginname', ''),
                    key='loginname', size=(30, 1))],
            [sg.Text('パスワード:', size=(14, 1)),
                sg.InputText(
                    oVals.get('pw', ''),
                    key='pw', size=(30, 1), password_char='*')],
            [sg.TabGroup([[
                sg.Tab('パスワードの変更', [
                    [sg.Text(' 新しいパスワードを入力して、\n[変更]ボタンを押してください。')],
                    [sg.Text('パスワード:', size=(14, 1)),
                        sg.InputText('', key='newpw', size=(30, 1),
                                     password_char='*')],
                    [sg.Button('変更', key='changePw', size=(10, 1))]
                ]),
                sg.Tab('ユーザの作成', [
                    [sg.Text(' 新しいログイン名と初期パスワードを入力して、\n'
                             '[登録]ボタンを押してください。')],
                    [sg.Text('接続ログイン名:', size=(14, 1)),
                        sg.InputText('', key='newloginname', size=(30, 1))],
                    [sg.Text('パスワード:', size=(14, 1)),
                        sg.InputText('', key='newloginpw', size=(30, 1),
                                     password_char='*')],
                    [sg.Button('登録', key='createLogin', size=(10, 1))]
                ]),
                sg.Tab('ユーザの削除', [
                    [sg.Text(' 削除対象のログイン名を入力して、\n'
                             '[削除]ボタンを押してください。')],
                    [sg.Text('接続ログイン名:', size=(14, 1)),
                        sg.InputText('', key='delloginname', size=(30, 1))],
                    [sg.Button('削除', key='deleteLogin', size=(10, 1))]
                ])
            ]], size=(510, 130))],
            [sg.Output(size=(70, 10))]
        ]

        self.window = sg.Window('Azure SQL Util?', layout)

    def main(self):
        # event loop
        while True:
            try:
                event, values = self.window.read()

                if event == sg.WIN_CLOSED:
                    # valuesに値が入ってないため、保存できない。
                    break

                elif values['myMenu'] == '値を保存して終了':
                    with open('settings.pkl', 'wb') as f:
                        pickle.dump(values, f)
                    break

                elif values['myMenu'] == '必要ですか？':
                    sg.popup('詳しそうな方に訊いてください。', title="準備未済", modal=True)
                    continue

                elif event == 'changePw':
                    self.event_changePw(event, values)
                    continue

                elif event == 'createLogin':
                    self.event_createLogin(event, values)
                    continue

                elif event == 'deleteLogin':
                    self.event_deleteLogin(event, values)
                    continue

            except Exception as e:
                print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                      + ' ERROR ' + event)
                print(e)
                continue

        self.window.close()

    def event_changePw(self, event, values):
        conStr = self.CONNECT_STRING.format(
            servername=values['servername'],
            dbname='master',
            loginname=values['loginname'],
            pw=values['pw'])
        if self.DEBUG:
            print(conStr)
        queryStr = 'ALTER LOGIN [{loginname}] '\
            'WITH PASSWORD = \'{newpw}\' OLD_PASSWORD = \'{pw}\';'
        queryStr = queryStr.format(
            loginname=values['loginname'],
            newpw=values['newpw'],
            pw=values['pw'])
        if self.DEBUG:
            print(queryStr)
        with pyodbc.connect(conStr) as cnn:
            cur = cnn.cursor()
            cur.execute(queryStr)
            cnn.commit()
        print("パスワードの変更 完了！")

    def event_createLogin(self, event, values):
        conStr = self.CONNECT_STRING.format(
            servername=values['servername'], dbname='master',
            loginname=values['loginname'], pw=values['pw'])
        if self.DEBUG:
            print(conStr)
        queryStr = 'CREATE LOGIN [{newloginname}]'\
            ' WITH PASSWORD = \'{newloginpw}\';'\
            'CREATE USER [{newloginname}];'
        queryStr = queryStr.format(
            newloginname=values['newloginname'],
            newloginpw=values['newloginpw'])
        if self.DEBUG:
            print(queryStr)
        with pyodbc.connect(conStr) as cnn:
            cur = cnn.cursor()
            cur.execute(queryStr)
            cnn.commit()

        conStr = self.CONNECT_STRING.format(
            servername=values['servername'], dbname=values['dbname'],
            loginname=values['loginname'], pw=values['pw'])
        if self.DEBUG:
            print(conStr)
        queryStr = 'CREATE USER [{newloginname}];'\
            'EXEC sp_addrolemember \'db_owner\', \'{newloginname}\';'
        queryStr = queryStr.format(
            newloginname=values['newloginname'])
        if self.DEBUG:
            print(queryStr)
        with pyodbc.connect(conStr) as cnn:
            cur = cnn.cursor()
            cur.execute(queryStr)
            cnn.commit()
        print("ユーザの作成 完了！")

    def event_deleteLogin(self, event, values):
        conStr = self.CONNECT_STRING.format(
            servername=values['servername'], dbname=values['dbname'],
            loginname=values['loginname'], pw=values['pw'])
        if self.DEBUG:
            print(conStr)
        queryStr = 'DROP USER [{delloginname}];'
        queryStr = queryStr.format(
            delloginname=values['delloginname'])
        if self.DEBUG:
            print(queryStr)
        try:
            with pyodbc.connect(conStr) as cnn:
                cur = cnn.cursor()
                cur.execute(queryStr)
                cnn.commit()
        except Exception as e:
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                  + ' ERROR ' + event)
            print(e)

        conStr = self.CONNECT_STRING.format(
            servername=values['servername'],
            dbname='master',
            loginname=values['loginname'],
            pw=values['pw'])
        if self.DEBUG:
            print(conStr)
        queryStr = 'DROP USER [{delloginname}];'\
            'DROP LOGIN [{delloginname}]'
        queryStr = queryStr.format(
            delloginname=values['delloginname'])
        if self.DEBUG:
            print(queryStr)
        try:
            with pyodbc.connect(conStr) as cnn:
                cur = cnn.cursor()
                cur.execute(queryStr)
                cnn.commit()
            print("ユーザの削除 完了！")
        except Exception as e:
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                  + ' ERROR ' + event)
            print(e)


if __name__ == '__main__':
    azure_sql_util().main()
