PYTHON ?= python3

.PHONY: help version install lint format test coverage doc uml clean
# --- Help: show available commands ---
help:
	@echo "Available targets:"
	@echo "  make help      - Show this help message"
	@echo "  make version   - Show Python version"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make coverage  - Generate coverage report"
	@echo "  make lint      - Run linters (flake8 + pylint)"
	@echo "  make format    - Check code formatting (black)"
	@echo "  make doc       - Generate API documentation"
	@echo "  make uml       - Generate UML diagrams"
	@echo "  make clean     - Clean temporary files"

# --- Version: show Python version ---
version:
	@$(PYTHON) --version
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
# --- Generate UML diagrams ---
uml:
	@echo ">>> Generating UML diagrams"
	pyreverse -o dot -p pig_game pig_game
	dot -Tpng classes_pig_game.dot -o doc/uml/classes_pig_game.png
	dot -Tpng packages_pig_game.dot -o doc/uml/packages_pig_game.png
	@echo "UML diagrams saved to doc/uml/"
