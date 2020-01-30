#!/usr/bin/python3
"""
AirBnB App
"""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(x=None):
    """remove the current session"""
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """handle error"""
    e = jsonify({'error': 'Not found'})
    return(e)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_POST')

    app.run(host=host, port=port, threaded=True)
