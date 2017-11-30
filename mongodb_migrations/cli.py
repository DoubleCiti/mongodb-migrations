from __future__ import print_function

from mongodb_migrations.commands.migrate import MigrationManager


def main():
    manager = MigrationManager()
    manager.run()


if __name__ == '__main__':
    main()
