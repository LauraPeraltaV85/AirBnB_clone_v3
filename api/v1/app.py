#!/usr/bin/python3
"""
AirBnB App
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_404(error):
    """
    handle error
    """
    return(jsonify(error="Not found"), 404)


@app.teardown_appcontext
def remove_session(x=None):
    """
    remove the current session
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')

    app.run(host=host, port=port, threaded=True)
