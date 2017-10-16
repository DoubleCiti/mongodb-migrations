#!/bin/sh

which twine || echo "twine is needed, use pip install twine to install it" && exit 1

python setup.py sdist

python setup.py bdist_wheel

twine upload dist/*
