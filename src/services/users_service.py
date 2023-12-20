from models.Users import Users

def login(data:dict) -> dict|None:
    '''
    Check username, password and returns the api key for that user.
    If the credentials are wrong, returns None
    '''
    user = Users.query.filter(Users.username == data['username']).first()

    if user is None:
        return 
    
    if user.password == data['password']:
        return {
            'key': user.api_key
        }

    