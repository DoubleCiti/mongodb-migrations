import os
from itertools import takewhile
from datetime import datetime

import binascii

import re

from mongodb_migrations.commands import Base
from mongodb_migrations.config import LabelType

MIGRATION_TEMPLATE = """\"\"\"
Version: <current_version>
Description: <description>
Created at: <datetime> 
\"\"\"

from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):

    # current_version = <current_hash>
    # previous_version = <previous_hash>

    def upgrade(self):
        pass

    def downgrade(self):
        pass
"""


class Create(Base):

    migrations = {}

    def __init__(self, options, *args, **kwargs):
        super(Create, self).__init__(options, *args, **kwargs)
        self.check_required_args(['label_type', 'migrations_path'])

    def run(self):
        if self.config.label_type == LabelType.TIMESTAMP:
            current_label = "".join(list(takewhile(
                lambda x: x != '.',
                str(datetime.now().utcnow()).replace('-', '').replace(
                    ' ', '').replace(':', ''))))
        else:
            current_label = binascii.hexlify(os.urandom(8))

        if self.config.label_type == LabelType.HASH:
            self._discover_migration_files(self.config.migrations_path)
            migrations = self._get_migrations_in_order()
            if migrations:
                prev_label = "'%s'" % migrations[-1]
            else:
                prev_label = 'None'
            my_migration_temp = MIGRATION_TEMPLATE.replace(
                '<current_hash>', "'%s'" % current_label).replace(
                '<previous_hash>', prev_label).replace('# ', '')
        else:
            my_migration_temp = MIGRATION_TEMPLATE

        my_migration_temp = my_migration_temp.\
            replace('<current_version>', current_label). \
            replace('<description>', self.config.description). \
            replace('<datetime>', datetime.now().isoformat())

        with open(self.config.migrations_path + ('/%s_%s.py' % (
                current_label,
                self.config.description.title().
                replace(" ",""))), 'w+') as f:
            f.write(my_migration_temp)

    # FIXME: Should be generalized with Migration methods
    def _get_prev_current_migrations(self, fp):
        migration_module = self._get_module(fp)
        current = migration_module.Migration.current_version
        prev = migration_module.Migration.previous_version

        return prev, current

    # FIXME: Should be generalized with Migration methods
    def _get_module(self, fp):
        migration_module = __import__(fp[:-3])
        return migration_module

    # FIXME: Should be generalized with Migration methods
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

    # FIXME: Should be generalized with Migration methods
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
                prev, current = self._get_prev_current_migrations(fp)
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


