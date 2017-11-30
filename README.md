mongodb-migrations
------------------

MongoDB is a great NoSQL and schema-less database, but if already have data in database and you changed data schema, you need a migration tool to update your existing data.

## How to install

* use `pip`

    ```bash
    $ pip install mongodb-migrations
    ```

* from source code

    ```bash
    $ python setup.py install
    ```

## How to use it

### Create a new migration file

1. create a fold named `migrations`
2. create a python file with name like `20160320145400_description.py`
3. in `20160320145400_description.py` create a class named `Migration` and extends `BaseMigration`
4. implement `upgrade` method

> CLI creation coming soon

### Execute a migration

Use cli `mongodb-migrate` to run migrations

If you don't wish to use the CLI, you can override the MigrationManager -> create_config and then call MigrationManager -> run. Example execution:

```python
    manager = MigrationManager()
    manager.config.migrator_config = "foobar.ini"
    manager.config._from_ini()
    manager.run()
```

You can also use the same config to keep multiple keys, the manager allows you access by using:
```python
   ini_config_parser = manager.config.ini_parser
   ini_config_parser.get('foo','bar')
```

## Configuration

### In-line Parameters

* `--host <string>` Set the database hostname.
* `--port <integer>` Set the database port.
* `--database <string>` Select the database to migrate.
* `--migrations <string>` Set the folder where to look for migration files.
* `--downgrade` Indicates that the opration to be executed is a downgrade. If it is not present, an upgrade will be executed.
* `--labeltype [TIMESTAMP|HASH]` Indicates which label type is used in the migrations. If no one is indicated, TIMESTAMP will be set.

### In-line configuration example

`mongodb-migrations` will try to load `config.ini` first, if it's not found, default values will be used. If any command line argument is provided, it will override config from configuration file.

**Only database name is mandatory**

### config.ini example

```ini
[mongo]
host = 127.0.0.1
port = 27017
database = test
migrations = migrations
```

### command line arguments example

```bash
mongodb-migrate --host 127.0.0.1 --port 27017 --database test --migrations examples
```

## Example

Migration files are located in `examples`, run following command to run migrations:

```
$ MONGODB_MIGRATIONS_CONFIG=examples/config.ini mongodb-migrate
```

For Downgrading the migrations, you need to pass a command line switch `--downgrade`

## Getting involved

* if you find any bug or need anything, please log an issue here: [Issues](https://github.com/eXpandCC/mongodb-migrations/issues)

## Credits

* Based on [DoubleCiti/mongodb-migrations](https://github.com/DoubleCiti/mongodb-migrations)
* Reinforced by [eXpandCC](https://github.com/eXpandCC)
