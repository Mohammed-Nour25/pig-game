.PHONY: lint format test coverage clean

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

clean:
	@echo ">>> cleaning build/test artifacts"
	@rm -rf .pytest_cache htmlcov build dist *.egg-info
