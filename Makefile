# vim: set ts=8 noet:

SHELL := /bin/bash


test: install
	./venv/bin/python formats.py
	./venv/bin/python v221602m.py

lint:
	./venv/bin/flake8 *.py

install: venv

venv: requirements.txt
	[[ -d venv ]] || { virtualenv -p python3 venv || python3 -m venv venv; }
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	touch venv  # prevent target from being re-run unless requirements.txt changes

clean:
	$(RM) -r venv

distclean: clean

.PHONY: clean install
