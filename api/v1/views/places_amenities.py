#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def ametities_by_place(place_id):
    """This route return the all ametities by place"""
    place = storage.get(Place, place_id)
    if place is not None:
        if request.method == 'GET':
            all_amenities = place.amenities
            new_dict = []
            for v in all_amenities:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE', 'POST'])
def place_id_manage_amenities(place_id, amenity_id):
    """return place with the matching place_id"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity is not None:
        if amenity in place.amenities:
            if request.method == "DELETE":
                """ remove the amenity in the giving place_id """
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({})
            if request.method == 'POST':
                return make_response(jsonify(amenity.to_dict()), 200)
        elif amenity not in place.amenities:
            if request.method == 'POST':
                """ Add a new amenity in a giving place """
                place.amenities.append(amenity)
                storage.save()
                return make_response(jsonify(amenity.to_dict()), 201)
    return make_response(jsonify({"error": "Not found"}), 404)
