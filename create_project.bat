@echo off
rem
rem create python project skelton
rem
rem @author kazuhiko@jomura.net
rem @version 2022.04.01

where /q python || (
    echo "Please install python before execution."
    exit /b 1
)
if "%1"=="" (
    echo "Please specify the project name."
    exit /b 1
)
set PROJECT_NAME=%1

python -m pip install --user pipenv

md %PROJECT_NAME%\src\%PROJECT_NAME% %PROJECT_NAME%\tests %PROJECT_NAME%\.vscode

copy nul %PROJECT_NAME%\src\%PROJECT_NAME%\__init__.py
copy nul %PROJECT_NAME%\tests\__init__.py
rem for unittest but pytest
(
    echo {
    echo     "python.linting.flake8Enabled": true,
    echo     "python.testing.unittestArgs": [
    echo         "-v",
    echo         "-s",
    echo         "./tests",
    echo         "-p",
    echo         "test_*.py"
    echo     ],
    echo     "python.testing.pytestEnabled": false,
    echo     "python.testing.unittestEnabled": true
    echo }
) > %PROJECT_NAME%\.vscode\settings.json
(
    echo def main^(^):
    echo     print^('hello, %PROJECT_NAME%.'^)
    echo.
    echo.
    echo if __name__ == '__main__':
    echo     main^(^)
) > %PROJECT_NAME%\src\%PROJECT_NAME%\__main__.py
(
    echo import unittest
    echo # from unittest.mock import MagicMock
    echo from %PROJECT_NAME%.__main__ import main
    echo.
    echo.
    echo class Test__main__^(unittest.TestCase^):
    echo.
    echo     def test___main__^(self^):
    echo         main^(^)
) > %PROJECT_NAME%\tests\test___main__.py
rem (
rem     echo # PIPENV_VENV_IN_PROJECT=true
rem ) > %PROJECT_NAME%\.env
rem set PIPENV_VENV_IN_PROJECT=true   # for Windwos
(
    echo **/__pycache__/
    echo src/*.egg-info/
    echo build/
    echo dist/
    echo .env
    echo .venv*/
    echo .coverage
    echo coverage.xml
) > %PROJECT_NAME%\.gitignore
(
    echo coverage run --source=src\%PROJECT_NAME% --omit=*__main__.py --branch -m unittest ^& coverage report -m ^&^& coverage xml
) > %PROJECT_NAME%\check_coverage.bat
(
    echo %PROJECT_NAME%
    echo ==========
    echo.
    echo.
    echo.
    echo Usage
    echo -----
) > %PROJECT_NAME%\README.ja.md
(
    echo from setuptools import setup
    echo setup^(^)
) > %PROJECT_NAME%\setup.py
(
    echo # https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
    echo [metadata]
    echo name = %PROJECT_NAME%
    echo version = 0.0.1
    echo description = 
    echo long_description_content_type = text/markdown
    echo long_description = file: README.ja.md
    echo url = https://github.com/joumura/python_pieces/
    echo.
    echo [options]
    echo packages = find:
    echo package_dir =
    echo     =src
    echo install_requires =
    echo     # requests
    echo.
    echo [options.packages.find]
    echo where = src
) > %PROJECT_NAME%\setup.cfg
(
    echo pipenv install --dev -e .
) > %PROJECT_NAME%\install.bat
pushd %PROJECT_NAME%\
pipenv --three install --dev -e . flake8 coverage
pipenv shell
