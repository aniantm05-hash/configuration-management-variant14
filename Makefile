.PHONY: run fixtures test

run:
	python3 -m src.main

fixtures:
	python3 -m src.fixtures

test:
	python3 -m unittest discover -s tests -v
