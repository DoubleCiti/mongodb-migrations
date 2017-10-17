from __future__ import print_function
from .config_parser import Configuration
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

    def __init__(self):
        self.create_config()

    def create_config(self):
        self.config = Configuration()
        if self.config.migrator_config != None:
            self.config.from_ini()
        else:
            self.config.from_console()


    def run(self):
        self.db = self._get_mongo_database(self.config.mongo_host, self.config.mongo_port, self.config.mongo_database)
        files = os.listdir(self.config.mongo_migrations_path)
        migrations = []
        for f in files:
            result = re.match('^\d+\.py$', f)
            if result:
                migrations.append(f)

        database_migrations = self._get_migration_names()
        database_migration_names = [migration['migration_datetime'] for migration in database_migrations]
        migration_names = ['%s' % migration.split('.')[0] for migration in migrations]
        if set(database_migration_names) - set(migration_names):
            print("migrations doesn't match")
            sys.exit(1)
        last_migration = None
        if database_migration_names:
            last_migration = database_migration_names[0]
            print("Found previous migrations, last migration is version: %s" % last_migration)
        else:
            print("No previous migrations found")

        sys.path.insert(0, self.config.mongo_migrations_path)
        for migration_name in migration_names:
            if not last_migration or migration_name > last_migration:
                print("Trying to migrate version: %s" % migration_name)
                try:
                    module = __import__(migration_name)
                    migration_object = module.Migration(host=self.config.mongo_host,
                                                        port=self.config.mongo_port,
                                                        database=self.config.mongo_database)
                    migration_object.upgrade()
                except Exception as e:
                    print("Failed to migrate version: %s" % migration_name)
                    print("%s" % e.message)
                    sys.exit(1)
                print("Succeed to migrate version: %s" % migration_name)
                self._create_migration(migration_name)

    def _get_migration_names(self):
        return self.db.database_migrations.find().sort('migration_datetime', pymongo.DESCENDING)

    def _create_migration(self, migration):
        self.db.database_migrations.save({'migration_datetime': migration,
                                     'created_at': datetime.now()})

    def _get_mongo_database(self, host, port, database):
        client = pymongo.MongoClient(host=host, port=port)
        return client[database]


def main():
    manager = MigrationManager()
    manager.run()
