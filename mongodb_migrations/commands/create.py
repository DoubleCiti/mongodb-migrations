import os
from itertools import takewhile
from datetime import datetime

import binascii

from mongodb_migrations.commands import Base
from mongodb_migrations.config import LabelType

MIGRATION_TEMPLATE = """
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):

    current_version = '<hash_current>'
    previous_version = '<hash_previous>'

    def upgrade(self):
        pass

    def downgrade(self):
        pass
"""


class Migrate(Base):

    def __init__(self, options, *args, **kwargs):
        super(Migrate, self).__init__(options, *args, **kwargs)
        self.check_required_args(['label_type', 'migrations_path'])

    def run(self):
        if self.config.label_type == LabelType.TIMESTAMP:
            current_label = "".join(list(takewhile(
                lambda x: x != '.',
                str(datetime.now().utcnow()).replace('-', '').replace(
                    ' ', '').replace(':', ''))))
        else:
            current_label = binascii.hexlify(os.urandom(8))

        with open(self.config.migrations_path + ('/%s_%s.py' % (
                current_label, self.config.description)), 'w+') as f:
            if self.config.label_type == LabelType.HASH:
                from mongodb_migrations.commands.migrate import Migrate
                Mi
                prev_label =
                my_migration_temp = \
                    MIGRATION_TEMPLATE.replace('<hash_current>', current_label)
                my_migration_temp = \
                    my_migration_temp.replace('<hash_previous>', prev_label)
            f.write(my_migration_temp)


