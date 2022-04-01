coverage run --source=src\tornado_authex --omit=*__main__.py --branch -m unittest & coverage report -m && coverage xml
