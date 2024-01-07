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


@app_views.route('/places_search', strict_slashes=False,
                 methods=['POST'])
def places_search():
    """This route return the all places by citie"""
    if request.method == 'POST':
        data = request.json
        if not data:
            return make_response(jsonify("Not a JSON"), 400)
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])
        if not states and not cities and not amenities:
            places = storage.all(Place).values()
            return jsonify([place.to_dict() for place in places])
        place_ids = set()
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                place_ids.update(place.id for city in state.cities
                                 for place in city.places)
        for city_id in cities:
            city = storage.get("City", city_id)
            if city:
                place_ids.update(place.id for place in city.places)
        places = [storage.get("Place", placeId).to_dict() for placeId
                  in place_ids if storage.get("Place", placeId)]
        if amenities:
            amenities_set = set(amenities)
            places = [place.to_dict() for place in places if
                      amenities_set.issubset(place.amenities)]
        print(len(places))
        return jsonify(places)
    return make_response(jsonify({"error": "Not found"}), 404)
