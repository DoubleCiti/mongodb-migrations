from __future__ import print_function
from .config import Configuration, Execution
import os
import sys
import re
from datetime import datetime

import pymongo


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

    def __init__(self):
        self.config = Configuration()

    def run(self):
        self.db = self._get_mongo_database(self.config.mongo_host, self.config.mongo_port, self.config.mongo_database,
                                           self.config.mongo_url)
        files = os.listdir(self.config.mongo_migrations_path)
        for file in files:
            result = re.match('^(\d+)[_a-z]*\.py$', file)
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
        {
            Execution.MIGRATE: self._do_migrate,
            Execution.DOWNGRADE: self._do_rollback
        }[self.config.execution]()

    def _do_migrate(self):
        for migration_datetime in sorted(self.migrations.keys()):
            if not self.database_migration_names or migration_datetime > self.database_migration_names[0]:
                print("Trying to upgrade version: %s" % self.migrations[migration_datetime])
                try:
                    module = __import__(self.migrations[migration_datetime])
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database,
                                                        url=self.config.mongo_url)
                    migration_object.upgrade()
                except Exception as e:
                    print("Failed to upgrade version: %s" % self.migrations[migration_datetime])
                    print(e.__class__)
                    if hasattr(e, 'message'):
                        print(e.message)
                    raise
                print("Succeed to upgrade version: %s" % self.migrations[migration_datetime])
                self._create_migration(migration_datetime)

    def _do_rollback(self):
        for migration_datetime in sorted(self.database_migration_names, reverse=True):
            if self.migrations[migration_datetime]:
                print("Trying to downgrade version: %s" % self.migrations[migration_datetime])
                try:
                    module = __import__(self.migrations[migration_datetime])
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database)
                    migration_object.downgrade()
                except Exception as e:
                    print("Failed to downgrade version: %s" % self.migrations[migration_datetime])
                    print(e.__class__)
                    if hasattr(e, 'message'):
                        print(e.message)
                    raise
                print("Succeed to downgrade version: %s" % self.migrations[migration_datetime])
                self._remove_migration(migration_datetime)

    def _get_migration_names(self):
        return self.db.database_migrations.find().sort('migration_datetime', pymongo.DESCENDING)

    def _create_migration(self, migration_datetime):
        self.db.database_migrations.save({'migration_datetime': migration_datetime,
                                          'created_at': datetime.now()})

    def _remove_migration(self, migration_datetime):
        self.db.database_migrations.remove({'migration_datetime': migration_datetime})

    def _get_mongo_database(self, host, port, database, url):
        if url:
            client = pymongo.MongoClient(url)
            return client.get_default_database()
        elif database:
            client = pymongo.MongoClient(host=host, port=port)
            return client[database]
        else:
            raise Exception('no database or url provided')


def main():
    manager = MigrationManager()
    manager.run()
