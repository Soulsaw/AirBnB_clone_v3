#!/usr/bin/python3
"""Doc module"""
from flask import jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<string:id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(id):
    """This route return the all reviews by place"""
    place = storage.get(Place, id)
    if place != None:
        if request.method == 'GET':
            all_reviews = place.reviews
            new_dict = []
            for v in all_reviews:
                new_dict.append(v.to_dict())
            return jsonify(new_dict)
        if request.method == 'POST':
            if not request.json:
                return make_response(jsonify("Not a JSON"), 400)
            elif not 'user_id' in request.json:
                return make_response(jsonify("Missing user_id"), 400)
            elif not 'text' in request.json:
                return make_response(jsonify("Missing text"), 400)
            attr = request.json
            user = storage.get(User, attr['user_id'])
            if user != None:
                attr['place_id'] = id
                review = Review(**attr)
                review.save()
                return make_response(jsonify(review.to_dict()), 201)
    return make_response(jsonify({"error": "Not Found"}), 404)

@app_views.route('/reviews/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def review(id):
    """return review with the match id"""
    review = storage.get(Review, id)
    if review != None:
        if request.method == "GET":
                return jsonify(review.to_dict())
        if request.method == "DELETE":
                storage.delete(review)
                storage.save()
                return jsonify({})
        if request.method == 'PUT':
                if not request.json:
                    return make_response(jsonify("Not a JSON"), 400)
                elif not 'text' in request.json:
                    return make_response(jsonify("Missing text"), 400)
                attr = request.json
                review.text = attr['text']
                storage.save()
                return make_response(jsonify(review.to_dict()), 200)
    return make_response(jsonify({"error": "Not Found"}), 404)