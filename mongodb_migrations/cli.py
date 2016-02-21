import argparse
import os
import sys
import re


parser = argparse.ArgumentParser(description="Mongodb migration parser")
parser.add_argument('--host', metavar='H', default='127.0.0.1',
                    help="host of MongoDB")
parser.add_argument('--port', type=int, metavar='p', default=27017,
                    help="port of MongoDB")
parser.add_argument('--database', metavar='d',
                    help="database of MongoDB")
parser.add_argument('--migrations', default='migrations',
                    help="directory of migration files")


def main():
    args = parser.parse_args()

    files = os.listdir(args.migrations)
    migrations = []
    for f in files:
        result = re.match('^\d+\.py$', f)
        if result:
            migrations.append(f)

    sys.path.insert(0, args.migrations)
    for migration in migrations:
        module = __import__('%s' % migration.split('.')[0])
        migration_object = module.Migration(host=args.host,
                                            port=args.port,
                                            database=args.database)
        migration_object.upgrade()
