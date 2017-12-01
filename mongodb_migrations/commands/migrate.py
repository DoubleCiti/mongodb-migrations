from mongodb_migrations.commands.base import Base
import os
import sys
import re
from datetime import datetime

import pymongo

from mongodb_migrations.config import Configuration, Execution, LabelType


class Migrate(Base):
    config = None
    db = None
    migrations = {}
    migrations_to_apply = []
    database_migration_names = None

    def __init__(self, options, *args, **kwargs):
        super(Migrate, self).__init__(options, *args, **kwargs)
        self.check_required_args(['database'])

    def run(self):
        # Connect to the DB
        self.db = self._get_mongo_database(
            self.config.host, self.config.port, self.config.database)

        # Discover the migration files
        sys.path.insert(0, self.config.migrations_path)
        self._discover_migration_files(self.config.migrations_path)

        migrations_in_order = self._get_migrations_in_order()

        print("Migrations found: %s" % " <-> ".join(migrations_in_order))

        current_version = self._get_current_version()
        if current_version:
            last_migration_idx = migrations_in_order.index(
                current_version)
        else:
            last_migration_idx = -1
        if self.config.execution == Execution.UPGRADE:
            self.migrations_to_apply = \
                migrations_in_order[last_migration_idx+1:]
        else:
            # Downgrade is applied by one step
            try:
                self.migrations_to_apply = \
                    migrations_in_order[
                        max(0, last_migration_idx-2):last_migration_idx+1]
                self.migrations_to_apply.reverse()
            except IndexError:
                self.migrations_to_apply = None

        self._migrate()
        sys.exit(0)

    def _discover_migration_files(self, migrations_path):
        try:
            files = os.listdir(migrations_path)
        except:
            raise Exception(
                "'%s' is not a valir migrations path" % migrations_path)

        for file in files:
            result = re.match('^([_a-zA-Z0-9]+)_[_a-zA-Z0-9]*\.py$', file)
            if result:
                self.migrations[result.group(1)] = file

    def _get_module(self, fp):
        migration_module = __import__(fp[:-3])
        return migration_module

    def _get_migration_instance(self, fp):
        migration_module = self._get_module(fp)
        migration_object = migration_module.Migration(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database)

        return migration_object

    def _migrate(self):
        if not self.migrations_to_apply:
            print("There's no migrations to be applied. DB up-to-date.")
        else:
            print("Migrations to be applied:\n%s\n" %
                  " -> ".join(self.migrations_to_apply))
        for migration_label in self.migrations_to_apply:
            file_to_apply = self.migrations[migration_label]
            print("> Trying to apply %s on version %s (file %s)" %
                  (self.config.execution, migration_label,
                   file_to_apply))
            try:
                migration_object = self._get_migration_instance(file_to_apply)
                if self.config.execution == Execution.UPGRADE:
                    migration_object.upgrade()
                    self._create_migration(
                        migration_label, self.config.execution)
                else:
                    migration_object.downgrade()
                    self._create_migration(
                        migration_label, self.config.execution)
                    self._create_migration(
                        self.migrations_to_apply[-1]
                        if len(self.migrations_to_apply) == 2
                        else None, self.config.execution)
            except Exception as e:
                print("Failed to apply version: %s" % file_to_apply)
                print(e.__class__)
                if hasattr(e, 'message'):
                    print(e.message)
                sys.exit(1)
            print("Successfully applied version %s" % file_to_apply)
            if self.config.execution == Execution.DOWNGRADE:
                break

    def _get_migration_names(self):
        return self.db.database_migrations.find().sort(
            'migration_label', pymongo.DESCENDING)

    def _create_migration(self, migration_label, execution):
        self.db.database_migrations.save(
            {'migration_label': migration_label,
             'created_at': datetime.now(),
             'execution': execution})

    def _remove_migration(self, migration_label):
        self.db.database_migrations.remove(
            {'migration_label': migration_label})

    def _get_mongo_database(self, host, port, database):
        client = pymongo.MongoClient(host=host, port=port)
        return client[database]

    def _get_migrations_in_order(self):
        """Returns a list of examples files in order to be applied"""

        migrations = []

        if not self.migrations:
            return migrations

        if self.config.label_type == LabelType.TIMESTAMP:
            migrations = sorted(self.migrations.keys())
        else:
            migrations_prev2current = {}
            for fp in self.migrations.values():
                prev, current = self._get_prev_current_migrations(
                    self.config.migrations_path + '/' + fp)
                migrations_prev2current[prev] = current

            last_mig = None
            for i in range(len(migrations_prev2current) + 1):
                next_mig = migrations_prev2current.get(last_mig, None)
                if not next_mig:
                    break
                migrations.append(next_mig)
                last_mig = next_mig
            else:
                raise Exception("One or more cycles are present in the "
                                "examples files")

        return migrations

    def _get_prev_current_migrations(self, fp):
        migration_module = self._get_module(fp)
        current = migration_module.Migration.current_version
        prev = migration_module.Migration.previous_version

        return prev, current

    def _get_current_version(self):
        versions = list(self.db.database_migrations.find().sort(
            'created_at', pymongo.DESCENDING))
        if versions:
            version = versions[0].get('migration_label') or \
                      versions[0].get('migration_datetime')
            return version
