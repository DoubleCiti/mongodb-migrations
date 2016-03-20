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
2. create a python file with name like `20160320145400.py`
3. in `20160320145400.py` create a class named `Migration` and extends `BaseMigration`
4. implement `upgrade` method
5. use cli `mongodb-migrate` to run migrations

## Example

## Getting involved

* if you find any bug or need anything, please log an issue here: [Issues](https://github.com/DoubleCiti/mongodb-migrations/issues)