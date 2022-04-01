coverage run --source=src\loggingex --omit=*__main__.py --branch -m unittest & coverage report -m && coverage xml
