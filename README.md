mongodb-migrations
------------------

MongoDB is a great NoSQL and schema-less database, but if already have data in database and you changed data schema, you need a migration tool to update your existing data.

## How to install

### From source code

    $ python setup.py install

## How to use it

### Create a new migration file

Run the command:

### From installation
    $ mongodb-migrate create --migrations examples/ --labeltype HASH --description "My new migration"
### From console, using python command
    $ python -m mongodb_migrations.cli create --migrations examples/ --labeltype HASH --description "My new migration"

It will generate a migration file in the folder indicated by `--migrations`, containing a template code.
Depending on the value of `--labeltype`, the migrations will be guided sorted by a timestamp in the file name or an unique hash written inside the code (previous_version/current_version class variables).
All you need to do is write the code inside `upgrade()` and `downgrade()` methods.


### Execute a migration

### From installation
Use cli `mongodb-migrate` to run migrations
#### Downgrade
    $ mongodb-migrate migrate downgrade --migrations examples/ --labeltype HASH --database fakedb
#### Upgrade
    $ mongodb-migrate migrate upgrade --migrations examples/ --labeltype HASH --database fakedb
#### Create new migration
    $ mongodb-migrate create --migrations examples/ --labeltype HASH --description "My new migration"

### From console, using python command
#### Downgrade
    $ python -m mongodb_migrations.cli migrate downgrade --migrations examples/ --labeltype HASH --database fakedb
#### Upgrade
    $ python -m mongodb_migrations.cli migrate upgrade --migrations examples/ --labeltype HASH --database fakedb
#### Create new migration
    $ python -m mongodb_migrations.cli create --migrations examples/ --labeltype HASH --description "My new migration"


## Command-line arguments

* `--host <string>` Set the database hostname.
* `--port <integer>` Set the database port.
* `--database <string>` Select the database to migrate.
* `--migrations <string>` Set the folder where to look for migration files.
* `--labeltype (TIMESTAMP|HASH)` Indicates which label type is used in the migrations. If no one is indicated, TIMESTAMP will be set.
* `--description "<string>"` Set the description in the creation of a migration file.

### Example

```bash
mongodb-migrate migrate upgrade --host 127.0.0.1 --port 27017 --database test --migrations examples
```


## File Configurations

### WARNING! Still not running well.

`mongodb-migrations` will try to load `config.ini` first, if it's not found,
default values will be used. If any command line argument is provided,
it will override the values taken from the configuration file.

### config.ini example

```ini
[mongo]
host = 127.0.0.1
port = 27017
database = test
migrations = migrations
```


## Getting involved

* To report bugs or present new ideas, please log an issue in [Issues](https://github.com/eXpandCC/mongodb-migrations/issues)

## Credits

* Based on [DoubleCiti/mongodb-migrations](https://github.com/DoubleCiti/mongodb-migrations)
* Reinforced by [eXpandCC](https://github.com/eXpandCC)
