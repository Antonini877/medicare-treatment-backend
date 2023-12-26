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
def login_route():
    data = request.get_json()
    
    authorization_data = login(data)
    
    if authorization_data is None:
        return jsonify({'message': 'Unauthorized access'}), 401

        
    return jsonify(authorization_data)
    
@app.route('/api/v1/occurrences',  methods=['POST', 'GET'], endpoint='occurrences')
@authenticated
def occurrences_route(user_id):
    
    if request.method == 'GET':
        return jsonify(get_occurrences_list(user_id))
    
    elif request.method == 'POST':
        data = request.get_json()
        write_occurrence(user_id, data)

        return jsonify({'message':'ok'})


@app.route('/api/v1/occurrences/grouped',  methods=['GET'],  endpoint='occurrences_grouped')
@authenticated
def occurrences_grouped_route(user_id):
    
    return jsonify(group_occorrences_day(user_id))
    
    



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
