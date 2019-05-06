.PHONY: test
test: develop
	@python setup.py test

.PHONY: develop
develop:
	@pip install -e .

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-pyc clean-build clean
clean: clean-build clean-pyc
