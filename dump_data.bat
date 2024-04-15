@echo off
python -m pipenv run python src\manage.py dumpdata --indent=4 --format=json dataStorage.Medicine > medicines.json
pause
