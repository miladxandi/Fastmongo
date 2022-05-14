from encodings.utf_8 import encode
import bcrypt
from bson import ObjectId
from fastapi import FastAPI, Response, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from starlette import status
from starlette.testclient import TestClient

from Helpers.Config.App import APP_KEY
from Helpers.Features.Functions import JsonGenerator
from Models.Access_Token import AccessToken
from Models.List import List, User
from Repository.AccessTokenRepository import AccessTokenRepository
from Repository.UserRepository import UserRepository
from Repository.ListRepository import ListRepository
from fastapi_login import LoginManager

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

manager = LoginManager(APP_KEY, token_url='/auth/token')


def get_user_by_access_token(access_token):
    access_token_object = AccessTokenRepository("AccessTokens")
    user = access_token_object.find_by_token(access_token)
    return ObjectId(user['_id']['$oid'])


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
    try:
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

        at = AccessToken(access_token=access_token, user_id=ObjectId(user['_id']['$oid']))
        AccessTokenRepo = AccessTokenRepository(table="AccessTokens")
        result = AccessTokenRepo.insert(at.dict())
        if result is not None:
            return JsonGenerator({'access_token': access_token, 'token_type': 'bearer'})
        else:
            Response.status_code = status.HTTP_401_UNAUTHORIZED
            return JsonGenerator(None, False, 401, "Unauthorized")
    except:
        Response.status_code = status.HTTP_401_UNAUTHORIZED
        return JsonGenerator(None, False, 401, "Unauthorized")


# %Lists%

@app.get("/lists")
def all_list():
    try:
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.all()

        for item in result:
            item['ownerId'] = None
            item.pop('ownerId')

        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)


@app.get("/lists/{id}")
def find_list(id: str):
    try:
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.find_by_id(id)
        result['ownerId'] = None
        result.pop('ownerId')
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)


@app.post("/lists")
def create_list(list: List, request: Request, str=Depends(oauth2_scheme)):
    try:
        token = request.headers.get('Authorization')
        list.ownerId = get_user_by_access_token(token)
        ListRepo = ListRepository(table="Lists")
        result = ListRepo.insert(list.dict())
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)


@app.put("/lists/{id}")
def update_list(id: str, list: List, request: Request, str=Depends(oauth2_scheme)):
    try:
        token = request.headers.get('Authorization')
        user_id = get_user_by_access_token(token)
        ListRepo = ListRepository(table="Lists")
        list_object = ListRepo.find_by_ownerId(user_id)
        if user_id.__str__() == list_object['ownerId']['$oid']:
            list.ownerId = get_user_by_access_token(token)
            result = ListRepo.update(id, list.dict())
            return JsonGenerator(result)
        else:
            Response.status_code = status.HTTP_401_UNAUTHORIZED
            return JsonGenerator(None, False, 401, "Unauthorized")
    except:
        Response.status_code = status.HTTP_401_UNAUTHORIZED
        return JsonGenerator(None, False, 401, "Unauthorized")


@app.delete("/lists/{id}")
def delete_list(id: str, request: Request, str=Depends(oauth2_scheme)):
    try:
        token = request.headers.get('Authorization')
        user_id = get_user_by_access_token(token)
        ListRepo = ListRepository(table="Lists")
        list_object = ListRepo.find_by_ownerId(user_id)
        if user_id.__str__() == list_object['ownerId']['$oid']:
            result = ListRepo.delete(id)
            return JsonGenerator(result)
        else:
            Response.status_code = status.HTTP_401_UNAUTHORIZED
            return JsonGenerator(None, False, 401, "Unauthorized")
    except:
        Response.status_code = status.HTTP_401_UNAUTHORIZED
        return JsonGenerator(None, False, 401, "Unauthorized")


# %Users%

@app.get("/profile")
def profile(id: str, user: User, str=Depends(oauth2_scheme)):
    try:
        UserRepo = UserRepository(table="Users")
        result = UserRepo.update(id, user)
        return JsonGenerator(result)
    except:
        return JsonGenerator("Something wrong happened", False)


@app.get("/users")
def all_user(str=Depends(oauth2_scheme)):
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
def update_user(id: str, user: User, str=Depends(oauth2_scheme)):
    UserRepo = UserRepository(table="Users")
    result = UserRepo.update(id, user.dict())
    return JsonGenerator(result)


@app.delete("/users/{id}")
def delete_user(id: str, str=Depends(oauth2_scheme)):
    UserRepo = UserRepository(table="Users")
    result = UserRepo.delete(id)
    return JsonGenerator(result)


# %Tests%

client = TestClient(app)


def test_all():
    response = client.get("/lists")
    assert response.status_code == 200
    assert response.json()['status'] == True
    assert len(response.json()['response']) >= 1
