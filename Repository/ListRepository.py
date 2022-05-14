from bson import ObjectId

from Helpers.Database.MainRepository import MainRepository


class ListRepository(MainRepository):
    def main(self):
        print(True)

    def find_by_ownerId(self, ownerId):
        return self.parse_json(self.table.find({"ownerId": ObjectId(ownerId)}))[0]
