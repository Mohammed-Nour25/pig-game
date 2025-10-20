.PHONY: lint format fmt test coverage clean doc uml

# --- Lint: flake8 + pylint (errors only) ---
lint:
	@echo ">>> flake8"
	flake8 .
	@echo ">>> pylint (errors only)"
	pylint -E pig_game

# --- Black (check only) ---
format:
	@echo ">>> black --check"
	black --check .

# --- Black (apply formatting) ---
fmt:
	@echo ">>> black (apply)"
	black .

# --- Run tests ---
test:
	pytest -q

# --- Coverage (HTML + console) ---
coverage:
	coverage run -m pytest
	coverage report -m
	coverage html
	@echo "HTML report: htmlcov/index.html"

# --- Docs (pdoc) ---
doc:
	@echo ">>> generating API docs with pdoc"
	@python -m pdoc pig_game -o doc/api

# --- UML diagrams (pyreverse) ---
uml:
	@echo ">>> generating UML with pyreverse"
	@pyreverse -AS -f ALL -o png -p pig_game pig_game
	@if exist classes_pig_game.png move /Y classes_pig_game.png doc\uml\classes_pig_game.png
	@if exist packages_pig_game.png move /Y packages_pig_game.png doc\uml\packages_pig_game.png

# --- Clean artifacts ---
clean:
	@echo ">>> cleaning build/test artifacts"
	@rm -rf .pytest_cache htmlcov build dist *.egg-info
