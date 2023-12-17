from app import app
from flask import  request
from controller.users_controller import *

@app.route('/')
def home():
    return {
        'status':'up'
    }

@app.route('/api/v1/users/auth', methods=['POST'])
def auth():
    data = request.get_json()
    return login(data)

if __name__ == '__main__':
    app.run(debug=True)
