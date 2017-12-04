from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):

    current_version = '20171017000000'
    previous_version = '20160320180710'

    def upgrade(self):
        for item in self.db.test_collection.find():
            item['new_column1'] = "fake_value"
            self.db.test_collection.save(item)

    def downgrade(self):
        self.db.test_collection.update_many(
            {}, {"$unset": {"new_column1": ""}})
