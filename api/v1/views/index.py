#!/usr/bin/python3
"""
Index
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def r_json():
    """
    return status
    """
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """
    returns class dictionary
    """
    cls_dict = {'amenities': storage.count('Amenity'),
                'cities': storage.count('City'),
                'places': storage.count('Place'),
                'reviews': storage.count('Review'),
                'states': storage.count('State'),
                'users': storage.count('User')}
    return jsonify(cls_dict)
