from Helpers.Database.MainRepository import MainRepository
from Models.User import User
from Repository.UserRepository import UserRepository


class AccessTokenRepository(MainRepository):
    def main(self):
        print(True)

    def find_by_token(self, access_token):
        try:
            data = self.parse_json(self.table.find({"access_token": access_token.replace("Bearer ", "")}))[0]
            UserRepo = UserRepository('Users')
            user = UserRepo.find_by_id(data['user_id'])
            return user
        except:
            return None
