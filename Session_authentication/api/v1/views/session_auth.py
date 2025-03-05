#!/usr/bin/env python3
""" Module of Session Auth
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """ view that handles all routes for the Session authentication
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})

    if not user or user == [] or user is None:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    json_user = jsonify(user[0].to_json())
    json_user.set_cookie(getenv("SESSION_NAME"), session_id)

    return json_user


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    else:
        return jsonify({}), 200
