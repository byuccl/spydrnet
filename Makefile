IN_ENV = if [ -e .venv/bin/activate ]; then . .venv/bin/activate; fi;

venv:
	python3 -m venv .venv
	$(IN_ENV) python3 -m pip install -U pip
	$(IN_ENV) pip3 install -r requirements.txt
	$(IN_ENV) pip3 install -e .

test:
	$(IN_ENV) python3 -m pytest -v
