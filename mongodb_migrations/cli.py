import argparse
import os
import sys
import re
from datetime import datetime

import pymongo

parser = argparse.ArgumentParser(description="Mongodb migration parser")
parser.add_argument('--host', metavar='H', default='127.0.0.1',
                    help="host of MongoDB")
parser.add_argument('--port', type=int, metavar='p', default=27017,
                    help="port of MongoDB")
parser.add_argument('--database', metavar='d',
                    help="database of MongoDB")
parser.add_argument('--migrations', default='migrations',
                    help="directory of migration files")


def get_migration_names(db):
    return db.database_migrations.find().sort('migration_datetime', pymongo.DESCENDING)


def get_mongo_database(host, port, database):
    client = pymongo.MongoClient(host=host, port=port)
    return client[database]


def create_migration(db, migration):
    db.database_migrations.save({'migration_datetime': migration,
                                 'created_at': datetime.now()})


def main():
    args = parser.parse_args()

    files = os.listdir(args.migrations)
    migrations = []
    for f in files:
        result = re.match('^\d+\.py$', f)
        if result:
            migrations.append(f)

    db = get_mongo_database(args.host, args.port, args.database)

    database_migrations = get_migration_names(db)
    database_migration_names = [migration['migration_datetime'] for migration in database_migrations]
    migration_names = ['%s' % migration.split('.')[0] for migration in migrations]
    if set(database_migration_names) - set(migration_names):
        print "migrations doesn't match"
        sys.exit(1)
    last_migration = None
    if database_migration_names:
        last_migration = database_migration_names[0]

    sys.path.insert(0, args.migrations)
    for migration_name in migration_names:
        if not last_migration or migration_name > last_migration:
            try:
                module = __import__(migration_name)
                migration_object = module.Migration(host=args.host,
                                                    port=args.port,
                                                    database=args.database)
                migration_object.upgrade()
            except Exception as e:
                print "%s" % e.message
                sys.exit(1)
            create_migration(db, migration_name)
