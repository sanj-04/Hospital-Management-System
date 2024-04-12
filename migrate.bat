@echo off
python -m pipenv run python src\manage.py makemigrations
python -m pipenv run python src\manage.py migrate
pause
