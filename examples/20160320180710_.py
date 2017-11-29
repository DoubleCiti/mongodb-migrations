from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):

    current_version = '20160320180710'
    previous_version = None

    def upgrade(self):
        self.db.test_collection.save({"new_column": "value"})

    def downgrade(self):
        self.db.test_collection.drop()
