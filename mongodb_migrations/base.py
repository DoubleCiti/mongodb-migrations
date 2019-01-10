import pymongo


class BaseMigration(object):
    def __init__(self,
                 host='127.0.0.1',
                 port='27017',
                 database=None,                 
                 auth_user=None,
                 auth_password=None,
                 url=None):
        if url and database and auth_user is not None: #provide auth_database in url (mongodb://mongohostname:27017/auth_database)
            client = pymongo.MongoClient(url, username=auth_user, password=auth_password)
            self.db = client.get_database(database)
        elif url:
            client = pymongo.MongoClient(url)
            self.db = client.get_default_database()
        elif database:
            client = pymongo.MongoClient(host=host, port=port)
            self.db = client[database]
        else:
            raise Exception('no database, url or auth_database in url provided')

    def upgrade(self):
        raise NotImplementedError

    def downgrade(self):
        raise NotImplementedError
