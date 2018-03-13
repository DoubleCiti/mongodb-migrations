from setuptools import setup, find_packages

setup(
    name='mongodb-migrations',
    version='0.5.1',
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
    install_requires=[
        'pymongo>=3.2.1',
        'configparser==3.5.0',
        'enum34==1.1.6',
    ],
    entry_points={
        'console_scripts': ['mongodb-migrate=mongodb_migrations.cli:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
