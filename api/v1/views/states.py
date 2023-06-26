#!/usr/bin/python3
"""Creating a new view for State objects """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)
    