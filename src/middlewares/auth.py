from flask import request, abort
from models.Users import Users


def authenticated(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('Api-Key')
        user = Users.query.filter(Users.api_key == api_key).first()
        
        if user is None:
            abort(401) 

        return func(user.id, *args, **kwargs)

    return wrapper