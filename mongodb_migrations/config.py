import argparse
import os
from configparser import ConfigParser
from enum import Enum

class Execution(Enum):
    DOWNGRADE = 'execution_downgrade'
    MIGRATE = 'execution_migrate'

class Configuration(object):
    config_file = os.getenv('MONGODB_MIGRATIONS_CONFIG', 'config.ini')
    mongo_host = '127.0.0.1'
    mongo_port = '27017'
    mongo_database = None
    mongo_migrations_path = 'migrations'
    execution = Execution.MIGRATE

    def __init__(self):
        self._from_ini()
        self._from_console()

        if not self.mongo_database:
            raise Exception("No database name is provided")

    def _from_console(self):
        self.arg_parser = argparse.ArgumentParser(description="Mongodb migration parser")

        self.arg_parser.add_argument('--host', metavar='H', default=self.mongo_host,
                            help="host of MongoDB")
        self.arg_parser.add_argument('--port', type=int, metavar='p', default=self.mongo_port,
                            help="port of MongoDB")
        self.arg_parser.add_argument('--database', metavar='d',
                            help="database of MongoDB", required=(self.mongo_database==None), default=self.mongo_database)
        self.arg_parser.add_argument('--migrations', default=self.mongo_migrations_path,
                            help="directory of migration files")
        self.arg_parser.add_argument('--downgrade', action='store_true',
                            default=False, help='Downgrade instead of upgrade')
        args = self.arg_parser.parse_args()

        self.mongo_host = args.host
        self.mongo_port = args.port
        self.mongo_database = args.database
        self.mongo_migrations_path = args.migrations
        if args.downgrade == True:
            self.execution = Execution.DOWNGRADE

    def _from_ini(self):
        self.ini_parser = ConfigParser(defaults={'host': self.mongo_host, 'port': self.mongo_port, 'migrations': self.mongo_migrations_path, 'database': self.mongo_database})

        try:
            fp = open(self.config_file)
        except Exception:
            pass
        else:
            with fp:
                self.ini_parser.readfp(fp)
                if not self.ini_parser.sections():
                    raise Exception("Cannot find %s or it doesn't have sections." % self.config_file)

                self.mongo_host = self.ini_parser.get('mongo', 'host')
                self.mongo_port = self.ini_parser.getint('mongo', 'port')
                self.mongo_database = self.ini_parser.get('mongo', 'database')
                self.mongo_migrations_path = self.ini_parser.get('mongo', 'migrations')
