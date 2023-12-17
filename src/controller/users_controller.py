from model.Users import Users

def login(data:dict) -> dict:
    user = Users.query.filter(Users.username == data['username']).first()
    if user.password == data['password']:
        return {
            'key': user.api_key
        }

