@echo off
python -m pipenv install -r requirements.txt
python -m pipenv run pip install -r requirements.txt
python -m pipenv lock
pause
