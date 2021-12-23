import sys
from setuptools import setup, find_packages

install_requires = [
    'pymongo>=3.2.1',
    'configparser>=3.5.0'
]

if sys.version_info < (3, 4):
    # Backport of Python 3.4 enums to earlier versions
    # reference: https://github.com/donnemartin/saws/commit/f109bc8f534905797ee44239cb766ea3de4ceb5d
    # credit to [donnemartin](https://github.com/donnemartin) and [geraldlnj](https://github.com/geraldlnj
    install_requires.append('enum34>=1.1.6')

setup(
    name='mongodb-migrations',
    version='1.1.1',
    description='A database migration tool for MongoDB',
    long_description=__doc__,
    url='https://github.com/DoubleCiti/mongodb-migrations',
    author='David Xie',
    author_email='david30xie@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['mongodb-migrate=mongodb_migrations.cli:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
