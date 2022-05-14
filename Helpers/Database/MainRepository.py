import json

from bson import json_util
from bson.objectid import ObjectId

from Helpers.Config.Database import DB_DATABASE
from Helpers.Database.MongoDB import Mongo


class MainRepository:
    database_object = None
    table = None

    def __init__(self, table):
        mongo = Mongo()
        self.database_object = mongo.connect(DB_DATABASE)
        self.table = self.database_object[table]

    def all(self):
        try:
            return self.parse_json(self.table.find({}))
        except:
            return None

    def insert(self, data: dict):
        try:
            return self.parse_json(self.table.insert_one(data).inserted_id)
        except:
            return None

    def find_by_id(self, id):
        try:
            return self.parse_json(self.table.find({"_id": ObjectId(id)}))
        except:
            return None

    def update(self, id, data):
        try:
            return self.parse_json(self.table.find_one_and_update({"_id": ObjectId(id)}, {"$set": data}))
        except:
            return None

    def delete(self, id):
        try:
            return self.parse_json(self.table.find_one_and_delete({"_id": ObjectId(id)}))
        except:
            return None

    def parse_json(self, data):
        return json.loads(json_util.dumps(data))
