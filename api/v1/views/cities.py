#!/usr/bin/python3
"""cities attribute"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """get city information for all cities in a specified state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get city information for specified city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())