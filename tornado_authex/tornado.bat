@echo off
rem DUKE LDAP接続情報 (passwordは"py crypt.py tgpower ${password}"で暗号化)
set LDAP_CONN_INFO=3069425 Y2e5CvkfZSRgcNpNrkIQLg==

py server.py
rem py server_basicauth.py
rem py server_bearerauth.py
