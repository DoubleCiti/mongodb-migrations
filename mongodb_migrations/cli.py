from __future__ import print_function

import os
import re
import sys
from datetime import datetime

import pymongo

from .config import Configuration, Execution


# TODO:
# split command to create and upgrade
# create:
#     create a file in custom folder
# upgrade:
#     run migration files from custom folder
class MigrationManager(object):
    config = None
    db = None
    migrations = {}
    database_migration_names = None

    def __init__(self, config=Configuration()):
        self.config = config

    def run(self):
        self.db = self._get_mongo_database(self.config.mongo_host, self.config.mongo_port, self.config.mongo_database,
                                           self.config.mongo_username, self.config.mongo_password,
                                           self.config.mongo_url)
        files = os.listdir(self.config.mongo_migrations_path)
        for file in files:
            result = re.match('^(\d+)[_a-z\d]*\.py$', file)
            if result:
                self.migrations[result.group(1)] = file[:-3]

        database_migrations = self._get_migration_names()
        self.database_migration_names = [migration['migration_datetime'] for migration in database_migrations]
        if set(self.database_migration_names) - set(self.migrations.keys()):
            print("migrations doesn't match")
            sys.exit(1)
        if self.database_migration_names:
            print("Found previous migrations, last migration is version: %s" % self.database_migration_names[0])
        else:
            print("No previous migrations found")

        sys.path.insert(0, self.config.mongo_migrations_path)
        {Execution.MIGRATE: self._do_migrate, Execution.DOWNGRADE: self._do_rollback}[
            self.config.execution
        ](self.config.to_datetime, self.config.levels)

    def create_migration(self):
        if not os.path.exists(self.config.mongo_migrations_path):
            os.makedirs(self.config.mongo_migrations_path)

        if not self.config.description:
            print("Please provide a description for the migration using --description.")
            sys.exit(1)

        filename = "%s/%s_%s.py" % (
            self.config.mongo_migrations_path,
            datetime.now().strftime('%Y%m%d%H%M%S'),
            self.config.description)
        with open(filename, 'w') as f:
            f.write("from mongodb_migrations.base import BaseMigration\n\n\n")

            f.write("class Migration(BaseMigration):\n")

            f.write("    def upgrade(self):\n")
            f.write("        pass\n\n")

            f.write("    def downgrade(self):\n")
            f.write("        pass\n")

        print("Migration created: %s" % filename)

    def _do_migrate(self, to_datetime=None, levels=0):
        performed_migrations = 0
        for migration_datetime in sorted(self.migrations.keys()):
            if to_datetime and migration_datetime > to_datetime:
                break
            if not self.database_migration_names or migration_datetime > self.database_migration_names[0]:
                print("Trying to upgrade version: %s" % self.migrations[migration_datetime])
                try:
                    module = __import__(self.migrations[migration_datetime])
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database,
                                                        user=self.config.mongo_username,
                                                        password=self.config.mongo_password,
                                                        url=self.config.mongo_url)
                    if not self.config.dry_run:
                        migration_object.upgrade()
                except Exception as e:
                    print("Failed to upgrade version: %s" % self.migrations[migration_datetime])
                    print(e.__class__)
                    if hasattr(e, 'message'):
                        print(e.message)
                    raise
                print("Succeed to upgrade version: %s" % self.migrations[migration_datetime])
                performed_migrations += 1

                if not self.config.dry_run:
                    self._create_migration(migration_datetime)
                if levels > 0:
                    print(
                        "Performed migrations: {} of {}".format(
                            performed_migrations, levels
                        )
                    )
                if performed_migrations == levels:
                    break
        print("Performed migrations: {}".format(performed_migrations))

    def _do_rollback(self, to_datetime=None, levels=0):
        performed_migrations = 0
        for migration_datetime in sorted(self.database_migration_names, reverse=True):
            if to_datetime and migration_datetime <= to_datetime:
                break
            if self.migrations[migration_datetime]:
                print("Trying to downgrade version: %s" % self.migrations[migration_datetime])
                try:
                    module = __import__(self.migrations[migration_datetime])
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database,
                                                        user=self.config.mongo_username,
                                                        password=self.config.mongo_password,
                                                        url=self.config.mongo_url)
                    if not self.config.dry_run:
                        migration_object.downgrade()
                except Exception as e:
                    print("Failed to downgrade version: %s" % self.migrations[migration_datetime])
                    print(e.__class__)
                    if hasattr(e, 'message'):
                        print(e.message)
                    raise
                print("Succeed to downgrade version: %s" % self.migrations[migration_datetime])
                performed_migrations += 1
                if not self.config.dry_run:
                    self._remove_migration(migration_datetime)
                if levels > 0:
                    print(
                        "Performed downgrades: {} of {}".format(
                            performed_migrations, levels
                        )
                    )
                if performed_migrations == levels:
                    break
        print("Performed downgrades: {}".format(performed_migrations))

    def _get_migration_names(self):
        return self.db[self.config.metastore].find().sort('migration_datetime', pymongo.DESCENDING)

    def _create_migration(self, migration_datetime):
        self.db[self.config.metastore].insert_one({'migration_datetime': migration_datetime,
                                          'created_at': datetime.now()})

    def _remove_migration(self, migration_datetime):
        self.db[self.config.metastore].delete_one({'migration_datetime': migration_datetime})

    def _get_mongo_database(self, host, port, database, user, password, url):
        if url and database and user is not None: #provide auth_database in url (mongodb://mongohostname:27017/auth_database)
            client = pymongo.MongoClient(url, username=user, password=password)
            return client.get_database(database)
        elif url:
            client = pymongo.MongoClient(url)
            return client.get_default_database()
        elif database:
            client = pymongo.MongoClient(host=host, port=port)
            return client[database]
        else:
            raise Exception('no database, url or auth_database in url provided')


def main():
    config = Configuration()
    config.from_console()
    manager = MigrationManager(config)
    manager.run()

def create_migration():
    config = Configuration()
    config.from_console()
    manager = MigrationManager(config)
    manager.create_migration()
