import os
from configparser import ConfigParser
from enum import Enum


class Execution(Enum):
    DOWNGRADE = 'DOWNGRADE'
    UPGRADE = 'UPGRADE'


class LabelType(Enum):
    HASH = 'hash'
    TIMESTAMP = 'timestamp'


class Configuration(object):
    config_file = os.getenv('MONGODB_MIGRATIONS_CONFIG', 'config.ini')
    host = '127.0.0.1'
    port = 27017
    database = None
    migrations_path = 'migrations'
    execution = Execution.UPGRADE
    label_type = LabelType.TIMESTAMP
    description = ''

    def __init__(self, options, args, kwargs):
        self._from_ini()
        self._from_console(options, args, kwargs)

    def _from_console(self, options, args, kwargs):
        self.host = options.get('--host', None) or self.host
        self.port = options.get('--port', self.port)
        self.database = options.get('--database', None) or self.database
        self.database = options.get('--description', None) or self.description
        self.migrations_path = \
            options.get('--migrations', None) or self.migrations_path
        if options.get('upgrade', None) or options.get('downgrade', None):
            self.execution = Execution.UPGRADE if options.get('upgrade', None) \
                else Execution.DOWNGRADE
        if options.get('--label-type', None):
            self.label_type = LabelType.HASH if \
                options.get('--label-type', None) == 'HASH' \
                else LabelType.TIMESTAMP

    def _from_ini(self):
        self.ini_parser = ConfigParser(
            defaults={'host': self.host, 'port': self.port,
                      'migrations': self.migrations_path,
                      'database': self.database})

        try:
            fp = open(self.config_file)
        except Exception:
            pass
        else:
            with fp:
                self.ini_parser.readfp(fp)
                if not self.ini_parser.sections():
                    raise Exception(
                        "Cannot find %s or it doesn't have sections." %
                        self.config_file)

                self.host = self.ini_parser.get('mongo', 'host')
                self.port = self.ini_parser.getint('mongo', 'port')
                self.database = self.ini_parser.get('mongo', 'database')
                self.migrations_path = \
                    self.ini_parser.get('mongo', 'migrations')
