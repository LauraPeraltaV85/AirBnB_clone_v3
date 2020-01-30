#!/usr/bin/python3
"""
Places
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """method that retrieves a list of all places"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    places = my_city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places_by_id(place_id):
    """method that retrieves a place filter by id"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_places_by_id(place_id):
    """method that deletes a place by id"""
    delete_place = storage.get('Place', place_id)
    if not delete_place:
        abort(404)
    else:
        delete_place.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """method to post a new place"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    my_user = storage.get('User', request.json['user_id'])
    if my_user is None:
        abort(404)
    new_place = request.get_json()
    if new_place is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, 'Missing user_id')
    if 'name' not in new_place:
        abort(400, 'Missing name')
    new_place = Place(name=request.json['name'],
                      city_id=city_id, user_id=request.json['user_id'])
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """method to update/put a place by id"""
    req_place = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_place = storage.get('Place', place_id)
    if mod_place is None:
        abort(404)
    for key in req_place:
        if key == 'id' or key == 'user_id' or\
           key == 'city_id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_place, key, req_place[key])
    storage.save()
    return jsonify(mod_place.to_dict()), 200
