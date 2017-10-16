import argparse
import os
from configparser import ConfigParser

class Configuration(object):
  migrator_config = None
  mongo_host = '127.0.0.1'
  mongo_port = 27017
  mongo_database = None
  mongo_migrations_path = 'migrations'

  def from_console(self):
    parser = argparse.ArgumentParser(description="Mongodb migration parser")
    parser.add_argument('--host', metavar='H', default=self.mongo_host,
                    help="host of MongoDB")
    parser.add_argument('--port', type=int, metavar='p', default=self.mongo_port,
                    help="port of MongoDB")
    parser.add_argument('--database', metavar='d',
                    help="database of MongoDB")
    parser.add_argument('--migrations', default=self.mongo_migrations_path,
                    help="directory of migration files")
    args = parser.parse_args()

    self.mongo_host = args.host
    self.mongo_port = args.port
    self.mongo_database = args.database
    self.mongo_migrations_path = args.migrations

  def from_ini(self):

    parser = ConfigParser()

    parser.read(self.migrator_config)
    if not parser.sections():
      raise Exception("Conf file not found or it doesn't have sections.")
    self.mongo_host = parser.get('mongo', 'host')
    self.mongo_port = parser.getint('mongo', 'port')
    self.mongo_database = parser.get('mongo', 'database')
    self.mongo_migrations_path = parser.get('mongo', 'migrations')
