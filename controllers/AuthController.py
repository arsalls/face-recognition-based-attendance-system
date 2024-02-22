import datetime
import os
from flask import request, session
from models.Users import Users
from utilities.errors import unhandled, invalid
from utilities.helpers import success, fail


def register_user():
    try:
        _json = request.json
        if _json:
            name = _json.get('name')
            email = _json.get('email')
            password = _json.get('password')
            isUser = Users.check_user(email=email)
            if isinstance(isUser, Exception): raise isUser
            if not isUser:
                user_id = Users.insert_user(name=name, email=email, password=password)
                if isinstance(user_id, Exception): raise user_id

                response = success(data={"message": "User registered and Successfully logged In....."})
                session['user'] = user_id
                response.set_cookie("user", user_id,
                                    expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("SESSION_EXPIRY_MINUTES"))))
                return response
            else:
                return fail(data={"message": "user already exists"}, status_code=200)
        return unhandled("invalid request")
    except Exception as e:
        return unhandled(e)

def login():
    try:
        _json = request.json
        if _json:
            email = _json.get('email')
            password = _json.get('password')
            if not (email and password):
                return fail(data={"message": "invalid request"}, status_code=200)

            if not Users.check_user(email=_json.get('email')):
                return fail(data={"message": "user not found"}, status_code=200)

            user = Users.get_users(email=email, password=password)
            if isinstance(user, Exception): raise user

            if user:
                response = success(data={"message": "User Successfully logged In....."})
                session['user'] = user.get('id')
                response.set_cookie("user", user.get('id'),
                                    expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv("SESSION_EXPIRY_MINUTES"))))
                return response
            else:
                return fail(data={"message": "Wrong password"}, status_code=200)
        return fail(data={"message": "payload is missing"}, status_code=200)
    except Exception as e:
        return unhandled(e)
