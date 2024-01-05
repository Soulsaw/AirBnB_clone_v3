#!/usr/bin/python3
"""Doc module"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """Doc route status"""
    json_status = {"status": "OK"}
    return jsonify(json_status)
