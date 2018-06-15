
all: build start

build:
	virtualenv .venv --python=python3.6
	.venv/bin/pip install -r server/requirements.txt

start:
	ENV=LOCAL .venv/bin/python3 server/wsgi.py

test:
	dropdb movie_catalogue_test > /dev/null || true
	createdb movie_catalogue_test > /dev/null
	ENV=TEST .venv/bin/nosetests -v -s server/tests