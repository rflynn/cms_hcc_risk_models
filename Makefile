# vim: set ts=8 noet:

SHELL := /bin/bash


test: install
	./venv3/bin/python formats.py
	./venv3/bin/python v221602m.py

lint:
	./venv3/bin/flake8 *.py

install: venv3

venv3: requirements.txt
	[[ -d venv3 ]] || { virtualenv -p python3 venv3 || python3 -m venv venv3; }
	./venv3/bin/pip install --upgrade pip
	./venv3/bin/pip install -r requirements.txt
	touch venv3  # prevent target from being re-run unless requirements.txt changes

clean:
	$(RM) -r venv3

distclean: clean

.PHONY: clean install
