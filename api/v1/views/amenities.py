#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
""" from models.city import City
from models.review import Review
from models.place import Place
from models.user import User """


@app_views.route('/amenities', methods = ['GET', 'POST'])
def amenities():
    """Return a dictionary representation of all amenities"""
    if request.method == 'GET':
        all_amenities = storage.all(Amenity).values()
        new_dict = []
        for v in all_amenities:
            new_dict.append(v.to_dict())
        return jsonify(new_dict)
    
    if request.method == "POST":
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)
        elif not 'name' in request.json:
            return make_response(jsonify("Missing name"), 400)
        attr = request.json
        amenity = Amenity(**attr)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)

@app_views.route('/amenities/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_id(id):
    """return amenities with the match id"""
    amenity = storage.get(Amenity, id)
    if amenity != None:
        if request.method == "GET":
                return jsonify(amenity.to_dict())
        if request.method == "DELETE":
                storage.delete(amenity)
                storage.save()
                return jsonify({})
        if request.method == 'PUT':
                if not request.json:
                    return make_response(jsonify("Not a JSON"), 400)
                elif not 'name' in request.json:
                    return make_response(jsonify("Missing name"), 400)
                attr = request.json
                amenity.name = attr['name']
                storage.save()
                return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({"error": "Not Found"}), 404)