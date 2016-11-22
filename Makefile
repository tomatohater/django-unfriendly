clean:
	rm -rf dist
	rm -rf *.egg-info

build:
	python setup.py sdist

upload_test:
	python setup.py sdist upload -r pypitest

upload:
	python setup.py sdist upload -r pypi

test:
	python runtests.py
