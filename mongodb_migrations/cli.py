"""
mongodb-migrate

Usage:
  mongodb-migrate -h | --help
  mongodb-migrate --version
  mongodb-migrate migrate (upgrade|downgrade) --migrations=PATH [--database=DATABASENAME --labeltype=(TIMESTAMP|HASH) --host=HOSTNAME --port=NUMBER]
  mongodb-migrate create --migrations=PATH [--database=DATABASENAME --labeltype=(TIMESTAMP|HASH) --host=HOSTNAME --port=NUMBER --description=DESCRIPTION]

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --host <hostname>                 Set the database hostname.
  --port <portnumber>               Set the database port.
  --database <databasename>         Select the database to migrate.
  --migrations <path>               Set the folder where to look for migration files.
  --downgrade                       Indicates that the opration to be executed is a downgrade. If it is not present, an upgrade will be executed.
  --labeltype (TIMESTAMP|HASH)      Indicates which label type is used in the migrations. If no one is indicated, TIMESTAMP will be set.

Examples:
  mongodb-migrate migrate upgrade --host 127.0.0.1 --database testDB

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/eXpandCC/mongodb-migrations/issues
"""

from __future__ import print_function
from inspect import getmembers, isclass

from docopt import docopt
from mongodb_migrations import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            cmd_module = getattr(commands, k)
            commands = getmembers(cmd_module, isclass)
            command = \
                [command[1] for command in commands
                 if command[0] == str.title(k)]
            if not command:
                print("%s command doesn't exist" % k)
                exit(1)
            else:
                command = command[0]
            command = command(options)
            command.run()

    # manager = MigrationManager()
    # manager.run()


if __name__ == '__main__':
    main()
