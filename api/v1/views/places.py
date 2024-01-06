#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:id>/places', methods=['GET', 'POST'])
def places_by_citie(id):
    """This route return the all places by citie"""
    citie = storage.get(City, id)
    if citie != None:
        if request.method == 'GET':
            all_places = citie.places
            new_dict = []
            for v in all_places:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif not 'user_id' in request.json:
                return make_response(jsonify("Missing user_id"), 400)
            elif not 'name' in request.json:
                return make_response(jsonify("Missing name"), 400)
            attr = request.json
            user = storage.get(User, attr['user_id'])
            if user != None:
                attr['citie_id'] = id 
                place = Place(**attr)
                place.save()
                return make_response(jsonify(place.to_dict()), 201)
    return make_response(jsonify({"error": "Not Found"}), 404)

@app_views.route('/places/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def place_id(id):
    """return citie with the match id"""
    place = storage.get(Place, id)
    if place != None:
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
    return make_response(jsonify({"error": "Not Found"}), 404)