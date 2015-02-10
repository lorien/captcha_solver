flake:
	flake8 selector test

flake_verbose:
	flake8 selector test --show-pep8

test:
	run test

coverage:
	coverage erase
	coverage run --source=selector -m runscript.cli test
	coverage report -m

.PHONY: all build venv flake test vtest testloop cov clean doc
