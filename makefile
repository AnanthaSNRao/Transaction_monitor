PYTHON = python
VENV_DIR = .venv

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

install: venv
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."


run: install
	@echo "Running main.py..."
	$(VENV_DIR)/bin/python main.py

freeze:
	@echo "adding all packages to requirements.txt"
	$(VENV_DIR)/bin/pip freeze > requirements.txt

clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	rm -rf *.txt *.csv
	@echo "Virtual environment removed."

.PHONY: [venv, install, run, clean, freeze]