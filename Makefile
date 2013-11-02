
.PHONY: test
test: pep8
	python setup.py test

.PHONY: pep8
pep8:
	@flake8 * --ignore=F403,F401 --exclude=requirements.txt,*.pyc,*.md,Makefile,LICENSE,*.in,*.rst
