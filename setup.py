from setuptools import setup, find_packages

# get requirements
install_requires = []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        install_requires.append(line)

setup(
    name='mongodb-migrations',
    version='0.1.0',
    long_description=__doc__,
    url='https://github.com/DoubleCiti/daimaduan.com',
    author='David Xie',
    author_email='david.xie@me.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points = {
        'console_scripts': ['mongo-migrate=mongodb_migrations.cli:main'],
    }
)
