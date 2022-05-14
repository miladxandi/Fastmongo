from pydantic import EmailStr

from Helpers.Config.App import APP_KEY
from Helpers.Database.MainRepository import MainRepository
import bcrypt
from encodings.utf_8 import encode


class UserRepository(MainRepository):

    def insert(self, data: dict):
        try:
            password = encode(data['password'])[0]
            app_key = encode(APP_KEY)[0]
            hash_password = bcrypt.hashpw(password, app_key)
            data['password'] = hash_password.__str__()
            return self.parse_json(self.table.insert_one(data).inserted_id)
        except:
            return None

    def find_by_email(self, email: str):
        try:
            return self.parse_json(self.table.find({"email": email})[0])
        except:
            return None
