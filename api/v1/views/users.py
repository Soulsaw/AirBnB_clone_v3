#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods = ['GET', 'POST'])
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
        elif not 'email' in request.json:
            return make_response(jsonify("Missing email"), 400)
        elif not 'password' in request.json:
            return make_response(jsonify("Missing password"), 400)
        attr = request.json
        user = User(**attr)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(id):
    """return users with the match id"""
    user = storage.get(User, id)
    if user != None:
        if request.method == "GET":
                return jsonify(user.to_dict())
        if request.method == "DELETE":
                storage.delete(user)
                storage.save()
                return jsonify({})
        if request.method == 'PUT':
                if not request.json:
                    return make_response(jsonify("Not a JSON"), 400)
                elif not 'password' in request.json:
                    return make_response(jsonify("Missing password"), 400)
                attr = request.json
                user.password = attr['password']
                storage.save()
                return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"error": "Not Found"}), 404)