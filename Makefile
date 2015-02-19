flake:
	flake8 captcha_solver test script

flake_verbose:
	flake8 captcha_solver test script --show-pep8

test:
	run test

coverage:
	coverage erase
	coverage run --source=captcha_solver -m runscript.cli test
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	python setup.py sdist upload

.PHONY: all build venv flake test vtest testloop cov clean doc
