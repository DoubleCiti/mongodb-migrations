import pymongo


class BaseMigration(object):
    def __init__(self,
                 host='127.0.0.1',
                 port='27017',
                 database=None):
        if not database:
            raise Exception('no database selected!')

        client = pymongo.MongoClient(host=host, port=port)
        self.db = client[database]

    def upgrade(self):
        raise NotImplementedError

    def downgrade(self):
        raise NotImplementedError
