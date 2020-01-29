#!/usr/bin/python3
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(x=None):
    """remove the current session"""
    storage.close()


@app.errorhandler(404)
def error_404(e):
    e = jsonify({'error': 'Not found'})
    return(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
