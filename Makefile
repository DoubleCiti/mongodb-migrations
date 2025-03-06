.PHONY: all

all: test

setup:
	pip install -r requirements.txt

test:
	exit 0

publish:
	pip install -r requirements-dev.txt
	./publish.sh
