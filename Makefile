PYTHON ?= python3

.PHONY: install lint format test coverage clean doc

# --- Install dependencies ---
install:
	$(PYTHON) -m pip install -r requirements.txt

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

# --- Run tests ---
test:
	pytest -q

# --- Coverage (HTML + console) ---
coverage:
	coverage run -m pytest
	coverage report -m
	coverage html
	@echo "HTML report: htmlcov/index.html"

# --- Generate documentation ---
doc:
	$(PYTHON) -m pdoc pig_game -o doc/api

# --- Clean build/test artifacts ---
clean:
	@echo ">>> cleaning build/test artifacts"
	@rm -rf .pytest_cache htmlcov build dist *.egg-info

