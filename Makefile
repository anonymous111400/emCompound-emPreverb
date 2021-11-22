
PYTHON:=venv/bin/python

all: install run

run:
	@echo
	@echo "Running scripts..."
	@echo
	cat in/in.tsv | $(PYTHON) scripts/compound | $(PYTHON) scripts/connect_prev.py > out/out.tsv
	cat in/in.tsv | cut -d '	' -f 1,4- > in/before
	cat out/out.tsv | cut -d '	' -f 1,4- > out/after
	@echo
	@echo 'Compare `in/before` and `out/after` to see the results'
	@echo 'e.g. by using `tkdiff in/before out/after`.'
	@echo

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
	cd xtsv_patched ; ../venv/bin/python -m pip install . ; cd ..

clean:
	rm -rf venv scripts/__pycache__ scripts/*/__pycache__

