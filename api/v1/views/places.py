#!/usr/bin/python3
"""
Places api
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    get places by id
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    place_obj = city.places
    place_list = []
    for p in place_obj:
        place_list.append(p.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def place_id(place_id):
    """
    find a user by id
    """
    places = storage.get('Place', place_id)
    if places is not None:
        return jsonify(places.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    delete place id
    """
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    creates a new place
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)

    nw_place = Place(name=request.json['name'],
                     user_id=request.json['user_id'],
                     city_id=city_id)
    storage.new(nw_place)
    storage.save()
    return jsonify(nw_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """
    update_task
    """
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(places, key, data[key])
    storage.save()
    return jsonify(places.to_dict()), 200
