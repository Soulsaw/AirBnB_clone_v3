#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """Return a dictionary representation of all users"""
    if request.method == 'GET':
        all_users = storage.all(User).values()
        new_dict = []
        for v in all_users:
            new_dict.append(v.to_dict())
        return jsonify(new_dict)
    if request.method == "POST":
        if not request.json:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'email' not in request.json:
            return make_response(jsonify("Missing email"), 400)
        elif 'password' not in request.json:
            return make_response(jsonify("Missing password"), 400)
        attr = request.json
        user = User(**attr)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """return an user with the matching user_id"""
    user = storage.get(User, user_id)
    if user is not None:
        if request.method == "GET":
            return jsonify(user.to_dict())
        if request.method == "DELETE":
            storage.delete(user)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif 'password' not in request.json:
                return make_response(jsonify("Missing password"), 400)
            attr = request.json
            user.password = attr['password']
            storage.save()
            return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"error": "Not found"}), 404)
