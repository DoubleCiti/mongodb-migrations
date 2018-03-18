import pymongo


class BaseMigration(object):
    def __init__(self,
                 host='127.0.0.1',
                 port='27017',
                 database=None, url=None):
        if url:
            client = pymongo.MongoClient(url)
            self.db = client.get_default_database()
        elif database:
            client = pymongo.MongoClient(host=host, port=port)
            self.db = client[database]
        else:
            raise Exception('no database or url provided')

    def upgrade(self):
        raise NotImplementedError

    def downgrade(self):
        raise NotImplementedError
