#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.state import State
""" from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User """


@app_views.route('/states', methods = ['GET', 'POST'])
def states():
    """Return a dictionary representation of all states"""
    if request.method == 'GET':
        all_states = storage.all(State).values()
        new_dict = []
        for v in all_states:
            new_dict.append(v.to_dict())
        return jsonify(new_dict)
    
    if request.method == "POST":
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)
        elif not 'name' in request.json:
            return make_response(jsonify("Missing name"), 400)
        attr = request.json
        state = State(**attr)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def state_id(id):
    """return states with the match id"""
    state = storage.get(State, id)
    if state != None:
        if request.method == "GET":
                return jsonify(state.to_dict())
        if request.method == "DELETE":
                storage.delete(state)
                storage.save()
                return jsonify({})
        if request.method == 'PUT':
                if not request.json:
                    return make_response(jsonify("Not a JSON"), 400)
                elif not 'name' in request.json:
                    return make_response(jsonify("Missing name"), 400)
                attr = request.json
                state.name = attr['name']
                storage.save()
                return make_response(jsonify(state.to_dict()), 201)
    return make_response(jsonify({"error": "Not Found"}), 404)