#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<string:id>/cities', methods=['GET', 'POST'])
def cities_by_state(id):
    """This route return the all cities by state"""
    state = storage.get(State, id)
    if state != None:
        if request.method == 'GET':
            all_cities = state.cities
            new_dict = []
            for v in all_cities:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif not 'name' in request.json:
                return make_response(jsonify("Missing name"), 400)
            attr = request.json
            attr['state_id'] = id 
            city = City(**attr)
            city.save()
            return make_response(jsonify(city.to_dict()), 201)
    return make_response(jsonify({"error": "Not Found"}), 404)

@app_views.route('/cities/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def city_id(id):
    """return citie with the match id"""
    city = storage.get(City, id)
    if city != None:
        if request.method == "GET":
                return jsonify(city.to_dict())
        if request.method == "DELETE":
                storage.delete(city)
                storage.save()
                return jsonify({})
        if request.method == 'PUT':
                if not request.json:
                    return make_response(jsonify("Not a JSON"), 400)
                elif not 'name' in request.json:
                    return make_response(jsonify("Missing name"), 400)
                attr = request.json
                city.name = attr['name']
                storage.save()
                return make_response(jsonify(city.to_dict()), 201)
    return make_response(jsonify({"error": "Not Found"}), 404)