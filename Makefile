# vim: set ts=8 noet:


test: install
	@echo "TODO: add tests"

install: venv3

venv3: requirements.txt
	[[ -d venv3 ]] || { virtualenv -p python3 venv3 || python3 -m venv venv3; }
	./venv3/bin/pip install -r requirements.txt
	touch venv3  # prevent target from being re-run unless requirements.txt changes

clean:
	$(RM) -r venv3

distclean: clean

.PHONY: clean install
