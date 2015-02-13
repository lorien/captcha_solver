flake:
	flake8 captcha_solver test

flake_verbose:
	flake8 captcha_solver test --show-pep8

test:
	run test

coverage:
	coverage erase
	coverage run --source=captcha_solver -m runscript.cli test
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

.PHONY: all build venv flake test vtest testloop cov clean doc
