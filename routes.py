from encodings.utf_8 import encode

import bcrypt
from bson import ObjectId
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from Helpers.Config.App import APP_KEY
from Helpers.Features.Functions import JsonGenerator
from Models.Access_Tokens import AccessToken
from Models.List import List, User, EmailStr
from Repository.AccessTokenRepository import AccessTokenrepository
from Repository.UserRepository import UserRepository
from Repository.ListRepository import ListRepository
from fastapi_login import LoginManager

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

manager = LoginManager(APP_KEY, token_url='/auth/token')

@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    try:
        UserRepo = UserRepository(table="Users")
        result = UserRepo.find_by_email(email)
        return result
    except:
        return JsonGenerator("Something wrong happened", False)


@app.post('/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user

    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif not bcrypt.checkpw(password=encode(password)[0], hashed_password=encode(user['password'][2:-1])[0]):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )

    at = AccessToken()
    at.access_token = access_token
    at.user_id = ObjectId(user['_id'])


    print(at)

    AccessTokenRepo = AccessTokenrepository(table="access_tokens")
    result = AccessTokenRepo.insert(at.dict())
    print(result)
    return JsonGenerator({'access_token': access_token, 'token_type': 'bearer'})

# %Lists%

@app.get("/lists")
def all_list(str = Depends(oauth2_scheme)):
    try:
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.all()
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)

@app.get("/lists/{id}")
def find_list(id: str):
    try:
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.find_by_id(id)
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)

@app.post("/lists")
def create_list(list: List):
    try:
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.insert(list.dict())
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)

@app.put("/lists/{id}")
def update_list(id: str, list: List):
    ListRepo = ListRepository(table="Lists")
    result = ListRepo.update(id, list.dict())
    return JsonGenerator(result)

@app.delete("/lists/{id}")
def delete_list(id: str):
    ListRepo = ListRepository(table="Lists")
    result = ListRepo.delete(id)
    return JsonGenerator(result)


# %Users%

@app.get("/users")
def all_users():
    try:
        UserRepo = UserRepository(table="Users")
        result = UserRepo.all()
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)

@app.get("/users/{id}")
def find_user(id: str):
    try:
        UserRepo = UserRepository(table="Users")
        result = UserRepo.find_by_id(id)
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)

@app.post("/users")
def create_user(user: User):
    UserRepo = UserRepository(table="Users")
    result = UserRepo.insert(user.dict())
    return JsonGenerator(result)

@app.put("/users/{id}")
def update_user(id: str, user: User):
    UserRepo = UserRepository(table="Users")
    result = UserRepo.update(id, user.dict())
    return JsonGenerator(result)

@app.delete("/users/{id}")
def delete_user(id: str):
    UserRepo = UserRepository(table="Users")
    result = UserRepo.delete(id)
    return JsonGenerator(result)

