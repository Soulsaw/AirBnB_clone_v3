#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
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
        elif 'name' not in request.json:
            return make_response(jsonify("Missing name"), 400)
        attr = request.json
        state = State(**attr)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_id(state_id):
    """return states with the match state_id"""
    state = storage.get(State, state_id)
    if state is not None:
        if request.method == "GET":
            return jsonify(state.to_dict())
        if request.method == "DELETE":
            storage.delete(state)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif 'name' not in request.json:
                return make_response(jsonify("Missing name"), 400)
            attr = request.json
            state.name = attr['name']
            storage.save()
            return make_response(jsonify(state.to_dict()), 200)
    return make_response(jsonify({"error": "Not found"}), 404)
