#!/usr/bin/python3
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """method that retrieves a list of all states"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    cities = my_state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """method that retrieves a city filter by id"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """method that deletes a state by id"""
    delete_city = storage.get('City', city_id)
    if not delete_city:
        abort(404)
    else:
        delete_city.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city_by_state(state_id):
    """method to post a new city"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    new_city = request.get_json()
    if new_city is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_city:
        abort(400, 'Missing name')
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """method to update/put a state by id"""
    req_city = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_city = storage.get('City', city_id)
    if mod_city is None:
        abort(404)
    for key in req_city:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_city, key, req_city[key])
    storage.save()
    return jsonify(mod_city.to_dict()), 200
