.PHONY: flake flake_verbose coverage clean upload

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
	python setup.py sdist upload
