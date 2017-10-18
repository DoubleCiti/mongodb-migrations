#!/bin/sh

which twine > /dev/null 2>&1 || (echo "twine is needed, use pip install twine to install it" && exit 1)

rm -rf dist/ build/

python setup.py sdist && \
python setup.py bdist_wheel && \
twine upload dist/*
