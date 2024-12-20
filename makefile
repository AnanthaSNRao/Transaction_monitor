PYTHON = python3 #For MacOS default if on any other OS can be just python
VENV_DIR = .venv

clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	rm -rf anomaly_detection_summary.txt detailed_anomaly_detection.log *.csv
	@echo "Virtual environment removed."
	
venv: clean
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

install: venv
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

generate: install
	$(VENV_DIR)/bin/python ./utils/transation_generator.py

run: generate
	@echo "Running main.py..."
	$(VENV_DIR)/bin/python main.py

freeze:
	@echo "adding all packages to requirements.txt"
	$(VENV_DIR)/bin/pip freeze > requirements.txt

.PHONY: [venv, install, run, clean, freeze, generate]