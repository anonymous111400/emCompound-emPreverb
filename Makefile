
PYTHON:=venv/bin/python
SHELL:=/bin/bash

all: install run

run:
	@echo
	@echo "Running scripts..."
	@echo
	cat in/in.tsv | \
    $(PYTHON) scripts/compound | \
    sed "s/	$$/	./" | \
    $(PYTHON) scripts/preverb \
    > out/out.tsv
	cat in/in.tsv | cut -d '	' -f 1,4- > in/before
	cat out/out.tsv | cut -d '	' -f 1,4- > out/after
	@echo
	@echo 'Compare `in/before` and `out/after` to see the results'
	@echo 'e.g. by using `tkdiff in/before out/after`.'
	@echo
# using a sed hack for patch xtsv
# not to strip empty fields at the end of line

install:
	@echo
	@echo "Creating venv..."
	@echo
	rm -rf venv
	python3 -m venv venv
	@echo
	@echo "Installing required packages..."
	@echo
	venv/bin/python -m pip install -r requirements.txt 

clean:
	rm -rf venv scripts/__pycache__ scripts/*/__pycache__

evaluate:
	cd evaluation && $(SHELL) evaluate.sh

