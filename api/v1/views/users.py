#!/usr/bin/python3
"""Create a new view for User object that handles
all default RESTFul API actions."""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    all_users = []
    users = list(storage.all('User').values())
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>/', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    error_message = ""
    content = request.get_json(silent=True)
    if isinstance(content, dict):
        if "email" not in content.keys():
            error_message = "Missing email"
        elif "password" not in content.keys():
            error_message = "Missing password"
        else:
            user = User(**content)
            storage.new(user)
            storage.save()
            response = jsonify(user.to_dict())
            response.status_code = 201
            return response
    else:
        error_message = "Not a JSON"
    response = jsonify({"error": error_message})
    response.status_code = 400
    return response


@app_views.route('/users/<user_id>/', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get("User", user_id)
    if user:
        content = request.get_json(silent=True)
        if isinstance(content, dict):
            for key, value in content.items():
                if key not in ignore:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)
