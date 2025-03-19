#!/usr/bin/env python3
""" Basic flask app module"""


from auth import Auth
from flask import abort, Flask, jsonify, redirect, request
app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def basic():
    """ Basic app route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """End-point to register a user"""
    try:
        user = AUTH.register_user(request.form["email"],
                                  request.form["password"])
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """A login route for the app
    """
    user_email = request.form["email"]
    user_pwd = request.form["password"]
    if AUTH.valid_login(user_email, user_pwd):
        session_id = AUTH.create_session(user_email)
        json_response = jsonify({"email": user_email, "message": "logged in"})
        json_response.set_cookie("session_id", session_id)
        return json_response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """A log out route for the app"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Get the user profile"""
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token"""
    user_email = request.form["email"]
    if user_email is not None:
        try:
            reset_token = AUTH.get_reset_password_token(user_email)
            return jsonify({"email": user_email,
                            "reset_token": reset_token}), 200
        except ValueError:
            abort(403)
    abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Route to update users password"""
    email = request.form["email"]
    reset_token = request.form["reset_token"]
    new_password = request.form["new_password"]

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
