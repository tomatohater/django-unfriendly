clean:
	rm -rf dist
	rm -rf *.egg-info

build:
	python setup.py sdist

upload_test:
	python setup.py upload -r pypitest

upload:
	python setup.py upload -r pypi

test:
	python runtests.py
