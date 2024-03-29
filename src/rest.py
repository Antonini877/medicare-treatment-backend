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
        
        page = request.args.get('page')  
        page_size = request.args.get('pageSize')
        
        return jsonify(get_occurrences_list(user_id, page, page_size))
    
    elif request.method == 'POST':
        data = request.get_json()
        write_occurrence(user_id, data)

        return jsonify({'message':'ok'})


@app.route('/api/v1/occurrences/grouped/byday',  methods=['GET'],  endpoint='occurrences_grouped')
@authenticated
def occurrences_grouped_route(user_id):
    
    return jsonify(group_occurrences_day(user_id))
    
    
@app.route('/api/v1/occurrences/grouped/bydayperiod',  methods=['GET'],  endpoint='occurrences_grouped_day_period')
@authenticated
def occurrences_grouped_dayperiod_route(user_id):
    
    return jsonify(group_occurrences_day_period(user_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
