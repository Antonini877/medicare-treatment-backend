from app import app
from flask import  request, abort, jsonify
from middlewares.auth import authenticated
from services.users_service import *
from services.occurrences_service import *

@app.route('/')
def home():
    return {
        'status':'up'
    }

@app.route('/api/v1/users/login', methods=['POST'])
def auth():
    data = request.get_json()
    
    authorization_data = login(data)
    
    if authorization_data is None:
        return jsonify({'message': 'Unauthorized access'}), 401

        
    return jsonify(authorization_data)
    
@app.route('/api/v1/occurrences',  methods=['POST', 'GET'])
@authenticated
def occurrences(user_id):
    
    if request.method == 'GET':
        return jsonify(get_occurrences_list(user_id))
    
    elif request.method == 'POST':
        data = request.get_json()
        write_occurrence(user_id, data)

        return jsonify({'message':'ok'})




if __name__ == '__main__':
    app.run(debug=True)
