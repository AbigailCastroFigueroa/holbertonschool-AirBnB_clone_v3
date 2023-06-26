#!/usr/bin/python3
"""Creating a new view for State objects """

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)
