#!/usr/bin/python3
"""Doc module"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Doc route status"""
    json_status = {"status": "OK"}
    return jsonify(json_status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """stats route doc"""
    stats_dict = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    for k, v in stats_dict.items():
        stats_dict[k] = storage.count(v)
    return jsonify(stats_dict)
