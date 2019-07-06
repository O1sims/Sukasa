import hashlib, binascii, os

from uuid import uuid4
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView

from api.models.user import LoginModel, UserModel
from api.services.MongoService import MongoService
from api.services.RedisService import RedisService

from sukasa.config import MONGO_DB_INFO

 
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        hash_name='sha512', 
        password=password.encode('utf-8'),
        salt=salt, 
        iterations=100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        hash_name='sha512',
        password=provided_password.encode('utf-8'),
        salt=salt.encode('ascii'),
        iterations=100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class LoginView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = LoginModel

    @swagger_auto_schema(responses={200: "Success"})
    def post(self, request, *args, **kwargs):
        LoginModel(
            data=request.data).is_valid(
            raise_exception=True)
        users = MongoService().find_user(
            collection_name=MONGO_DB_INFO['userCollection'], 
            username=request.data['username'])
        if len(users) == 1 and verify_password(
            stored_password=users[0]['password'], 
            provided_password=request.data['password']):
            token = [str(uuid4()), "Successfully logged in!", 200]
            RedisService().set_token(
                redis_key=token[0])
        else:
            token = [None, "Unable to log in. Please check username and password.", 403]
        return Response(
            data={
                "token": token[0],
                "msg": token[1]
            },
            status=token[2])


class UserView(CreateAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = UserModel
        
    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        UserModel(
            data=request.data).is_valid(
            raise_exception=True)
        users = MongoService().find_user(
            collection_name=MONGO_DB_INFO['userCollection'], 
            username=request.data['username'])
        if len(users) == 0:
            request.data['password'] = hash_password(
                password=request.data['password'])
            MongoService().insert_to_collection(
                collection_name=MONGO_DB_INFO['userCollection'],
                data=request.data)
            status = [True, "Successfully created User", 201]
        else:
            status = [False, "Could not create User", 403]
        return Response(
            data={"success": status[0], "msg": status[1]},
            status=status[2])

