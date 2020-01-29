#!/usr/bin/python3
"""
State CRUD
"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """method that retrieves a list of all states"""
    all_states = storage.all('State')
    states_list = all_states.values()
    states_json = []
    for state in states_list:
        states_json.append(state.to_dict())
    return jsonify(states_json)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """method that retrieves a state filter by id"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_by_id(state_id):
    """method that deletes a state by id"""
    delete_state = storage.get('State', state_id)
    if not delete_state:
        abort(404)
    else:
        delete_state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """method to post a new state"""
    new_state = request.get_json()
    if new_state is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """method to update/put a state by id"""
    req_state = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_state = storage.get('State', state_id)
    if mod_state is None:
        abort(404)
    for key in req_state:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_state, key, req_state[key])
    storage.save()
    return jsonify(mod_state.to_dict()), 200
