#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_by_citie(city_id):
    """This route return the all places by citie"""
    citie = storage.get(City, city_id)
    if citie is not None:
        if request.method == 'GET':
            all_places = citie.places
            new_dict = []
            for v in all_places:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif 'user_id' not in request.json:
                return make_response(jsonify("Missing user_id"), 400)
            elif 'name' not in request.json:
                return make_response(jsonify("Missing name"), 400)
            attr = request.json
            user = storage.get(User, attr['user_id'])
            if user is not None:
                attr['citie_id'] = city_id
                place = Place(**attr)
                place.save()
                return make_response(jsonify(place.to_dict()), 201)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_id(place_id):
    """return citie with the matching place_id"""
    place = storage.get(Place, place_id)
    if place is not None:
        if request.method == "GET":
            return jsonify(place.to_dict())
        if request.method == "DELETE":
            storage.delete(place)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            attr = request.json
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
    return make_response(jsonify({"error": "Not found"}), 404)
