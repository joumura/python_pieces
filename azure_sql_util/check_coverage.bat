coverage run --source=src\azure_sql_util --omit=*__main__.py --branch -m unittest & coverage report -m && coverage xml
