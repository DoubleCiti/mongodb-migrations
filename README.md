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

1. create a fold named `migrations`
2. create a python file with name in form of `TIMESTAMP_description.py` , i.e.`20160320145400_description.py`, otherwise migration file won't be found.
3. in `20160320145400_description.py` create a class named `Migration` and extends `BaseMigration`
4. implement `upgrade` method
5. use cli `mongodb-migrate` to run migrations
6. `metastore` is an optional parameter of collection name where it stores the previous migrations

**Now there is an easier way to create a migration file, command `mongodb-migrate-create --description <description>` will create an empty migration file in `migrations` folder or the folder provided by `--migrations`.**

If you don't wish to use the CLI, you can override the MigrationManager -> create_config and then call MigrationManager -> run. Example execution:

```python
    manager = MigrationManager()
    manager.config.config_file = "foobar.ini"
    manager.config._from_ini()
    manager.run()
```

You can also use the same config to keep multiple keys, the manager allows you access by using:
```python
   ini_config_parser = manager.config.ini_parser
   ini_config_parser.get('foo','bar')
```

## Configuration

`mongodb-migrations` will try to load `config.ini` first, if it's not found, default values will be used. If any command line argument is provided, it will override config from configuration file.

**Database name or Url is mandatory**

### config.ini example

```ini
[mongo]
host = 127.0.0.1
port = 27017
database = test
migrations = migrations
metastore = database_migrations
```

### alternative config.ini example
```ini
[mongo]
url = mongodb://127.0.0.1:27017/test
migrations = migrations
```

### auth-db config.ini example
```ini
[mongo]
url = mongodb://127.0.0.1:27017/admin
username = admin
password = secret123
database = test
migrations = migrations
metastore = database_migrations
```

### command line arguments example

```bash
mongodb-migrate --host 127.0.0.1 --port 27017 --database test --migrations examples
```

### alternative command line example
```bash
mongodb-migrate --url mongodb://127.0.0.1:27017/test --migrations examples
```


## Example

Migration files are located in `examples`, run following command to run migrations:

```
$ MONGODB_MIGRATIONS_CONFIG=examples/config.ini mongodb-migrate
```

For Downgrading the migrations, you need to pass a command line switch `--downgrade`

To upgrade/downgrade only to a specific migration, use `--to_datetime`. This command will upgrade to the migration with prefix `20191115180633`:
```bash
mongodb-migrate --url mongodb://127.0.0.1:27017/test --migrations examples --to_datetime 20191115180633
```

To upgrade/downgrade only to specific levels, use `--levels`. This command will downgrade 2 levels from the current latest migration:
```bash
mongodb-migrate --url mongodb://127.0.0.1:27017/test --downgrade --migrations examples --levels 2
```

## Getting involved

* if you find any bug or need anything, please log an issue here: [Issues](https://github.com/DoubleCiti/mongodb-migrations/issues)

## Contributors

* [Rohit Garg](https://github.com/rohitggarg)
* [mpgalaxy](https://github.com/mpgalaxy)
