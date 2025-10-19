PYTHON ?= python

.PHONY: install test coverage lint fmt doc uml

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	coverage run -m pytest -q || true
	coverage report -m

coverage:
	coverage run -m pytest || true
	coverage report -m
	coverage html

lint:
	flake8 .
	pylint -E pig_game || true

fmt:
	black .

doc:
	$(PYTHON) -m pdoc pig_game -o doc/api

uml:
	pyreverse -AS -f ALL -o png -p pig_game pig_game
	if exist classes_pig_game.png move /Y classes_pig_game.png doc\uml\classes_pig_game.png
	if exist packages_pig_game.png move /Y packages_pig_game.png doc\uml\packages_pig_game.png
