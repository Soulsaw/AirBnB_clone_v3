#!/usr/bin/python3
"""Doc module"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User


@app_views.route('/status')
def status():
    """Doc route status"""
    json_status = {"status": "OK"}
    return jsonify(json_status)

@app_views.route('/stats')
def stats():
    """stats route doc"""
    stats_dict = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(stats_dict)

