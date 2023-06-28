#!/usr/bin/python3
"""Create a new view for User object that handles
all default RESTFul API actions."""

from flask import Blueprint, jsonify, request, abort
from datetime import datetime
from models import storage

users_bp = Blueprint('users', __name__)

users = []


class User:
    def __init__(self, email, password):
        self.id = len(users) + 1
        self.email = email
        self.password = password
        self.name = f"User {self.id}"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@users_bp.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """Retrieves the list of all User objects"""
    user = list(storage.all('User').values())
    for user in users:
        users.append(user.to_dict())
    return jsonify(users)


@users_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@users_bp.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        abort(404)
    users.remove(user)
    return jsonify({}), 200


@users_bp.route('/apDeletes a User objecti/v1/users', methods=['POST'])
def create_user():
    """Creates a User"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(data['email'], data['password'])
    users.append(user)
    return jsonify(user.to_dict()), 201


@users_bp.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.updated_at = datetime.now()
    return jsonify(user.to_dict()), 200
