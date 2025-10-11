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
	$(PYTHON) -m pylint.pyreverse -o png -p pig_game pig_game || true
	mkdir -p doc/uml
	if [ -f "classes_pig_game.png" ]; then mv -f classes_pig_game.png doc/uml/; fi
	if [ -f "packages_pig_game.png" ]; then mv -f packages_pig_game.png doc/uml/; fi
