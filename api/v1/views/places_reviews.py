#!/usr/bin/python3
"""Create a view for reviews related to the same place."""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def search_place_review(place_id):
    """Return a list of reviews link to a place."""
    selected_place = storage.get(Place, place_id)
    if not selected_place:
        abort(404)
    list_of_reviews = []
    for review in selected_place.reviews:
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_review(review_id):
    """Get a review by its id."""
    wanted_review = storage.get(Review, review_id)
    if not wanted_review:
        abort(404)
    return jsonify(wanted_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a given review using its id."""
    review_to_delete = storage.get(Review, review_id)
    if not review_to_delete:
        abort(404)
    storage.delete(review_to_delete)
    storage.save()
    return jsonify({}), 200
