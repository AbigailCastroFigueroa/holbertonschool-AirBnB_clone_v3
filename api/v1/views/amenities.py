#!/usr/bin/python3
"""Create a view for Amenity objects."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve a list of all the amenities."""
    amenities_list = []
    for item in storage.all("Amenity").values():
        amenities_list.append(item.to_dict())
    return jsonify(amenities_list)


@app_views.route('amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieve an amenity by its id."""
    specific_amenity = storage.get(Amenity, amenity_id)
    if not specific_amenity:
        abort(404)
    return jsonify(specific_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete selected amenity."""
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if not amenity_to_delete:
        abort(404)
    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new Amenity object."""
    if request.method == 'POST':
        content = request.get_json()
        if not content:
            abort(400, 'Not a JSON')
        if "name" not in content:
            abort(400, 'Missing name')
        new_amenity = Amenity(**content)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity), 201
