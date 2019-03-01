.PHONY: flake flake_verbose coverage clean upload pylint flake8 lint test

flake:
	flake8 captcha_solver test

flake_verbose:
	flake8 captcha_solver test --show-pep8

coverage:
	coverage erase
	coverage pytest
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	git push --tags; python setup.py sdist upload

pylint:
	pylint captcha_solver

flake8:
	flake8 captcha_solver

lint: pylint flake8

test:
	pytest
