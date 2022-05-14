from pymongo import MongoClient

from Helpers.Config.Database import DB_HOST, DB_PORT


class Mongo:
    client = None

    def connect(self, database):
        self.client = MongoClient(host=DB_HOST, port=DB_PORT)

        # Create the database for our example (we will use the same database throughout the tutorial
        return self.client[database]

    def close(self):
        self.client.close()
