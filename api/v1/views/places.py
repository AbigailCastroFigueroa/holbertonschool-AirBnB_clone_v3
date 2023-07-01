#!/usr/bin/python3
"""Places API routes"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """Show places by city's id."""
    city = storage.get(City, city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Show place by place's id."""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete place by id."""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a place"""
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': "Missing name"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    city = storage.get(City, city_id)
    if not city or not user:
        abort(404)
    if city:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" in content.keys():
                user = storage.get(User, content['user_id'])
                if user:
                    if "name" in content.keys():
                        place = Place(**content)
                        place.city_id = city_id
                        storage.new(place)
                        storage.save()
                        response = jsonify(place.to_dict())
                        response.status_code = 201
                        return response


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(place, name, value)
            storage.save()
            return jsonify(place.to_dict()), 200
