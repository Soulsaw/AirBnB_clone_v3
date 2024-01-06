#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<city_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(city_id):
    """This route return the all cities by state"""
    state = storage.get(State, city_id)
    if state is not None:
        if request.method == 'GET':
            all_cities = state.cities
            new_dict = []
            for v in all_cities:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify('Not a JSON'), 400)
            elif 'name' not in request.json:
                return make_response(jsonify('Missing name'), 400)
            attr = request.json
            state = storage.get(State, city_id)
            if state is not None:
                attr['state_id'] = city_id
                city = City(**attr)
                city.save()
                return make_response(jsonify(city.to_dict()), 201)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city_id(city_id):
    """return citie with the match city_id"""
    city = storage.get(City, city_id)
    if city is not None:
        if request.method == 'GET':
            return jsonify(city.to_dict())
        if request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify('Not a JSON'), 400)
            elif 'name' not in request.json:
                return make_response(jsonify('Missing name'), 400)
            attr = request.json
            city.name = attr['name']
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)
    return make_response(jsonify({"error": "Not found"}), 404)
