from __future__ import print_function
from .config import Configuration
import os
import sys
import re
import logging
from datetime import datetime

import pymongo

# TODO:
# split command to create and upgrade
# create:
#     create a file in custom folder
# upgrade:
#     run migration files from custom folder
class MigrationManager(object):
    logger = logging.getLogger("cli")
    config = None
    db = None
    migrations = {}
    database_migration_names = None

    def __init__(self):
        self.config = Configuration()

    def run(self):
        self.db = self._get_mongo_database(self.config.mongo_host, self.config.mongo_port, self.config.mongo_database)
        files = os.listdir(self.config.mongo_migrations_path)
        for file in files:
            result = re.match('^(\d+)[_a-z]*\.py$', file)
            if result:
                self.migrations[result.group(1)] = file[:-3]

        database_migrations = self._get_migration_names()
        self.database_migration_names = [migration['migration_datetime'] for migration in database_migrations]
        if set(self.database_migration_names) - set(self.migrations.keys()):
            self.logger.error("migrations doesn't match")
            sys.exit(1)
        if self.database_migration_names:
            self.logger.info("Found previous migrations, last migration is version: %s" % self.database_migration_names[0])
        else:
            self.logger.info("No previous migrations found")

        sys.path.insert(0, self.config.mongo_migrations_path)
        self._domigrate()

    def _domigrate(self):
        for migration_datetime in sorted(self.migrations.keys()):
            if not self.database_migration_names or migration_datetime > self.database_migration_names[0]:
                self.logger.info("Trying to migrate version: %s" % self.migrations[migration_datetime])
                try:
                    module = __import__(self.migrations[migration_datetime])
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database)
                    migration_object.upgrade()
                except Exception as e:
                    self.logger.error("Failed to migrate version: %s" % self.migrations[migration_datetime])
                    print("%s" % e.message)
                    sys.exit(1)
                self.logger.info("Succeed to migrate version: %s" % self.migrations[migration_datetime])
                self._create_migration(migration_datetime)

    def _get_migration_names(self):
        return self.db.database_migrations.find().sort('migration_datetime', pymongo.DESCENDING)

    def _create_migration(self, migration_datetime):
        self.db.database_migrations.save({'migration_datetime': migration_datetime,
                                     'created_at': datetime.now()})

    def _get_mongo_database(self, host, port, database):
        client = pymongo.MongoClient(host=host, port=port)
        return client[database]


def main():
    manager = MigrationManager()
    manager.run()
