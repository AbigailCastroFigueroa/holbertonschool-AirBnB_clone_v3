#!/usr/bin/python3
"""Creating a new view for State objects """

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """ focus on all the state object """

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        if 'name' not in data:
            return Response("Missing name", 400)
        state = State(name=data.get('name'))
        state.save()
        return jsonify(state.to_dict()), 201

    all_states = storage.all('State')
    states = []

    for state in all_states.values():
        states.append(state.to_dict())
    return jsonify(states)
