#!/usr/bin/env python3
"""
Main file
"""
import requests


session = requests.Session()


def register_user(email: str, password: str) -> None:
    """Function to test register user route"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/users", data=data)
    assert response.status_code == 200, "Unexpected: " + str(
        response.status_code)

    expected_payload = {"email": email, "message": "user created"}
    assert response.json() == expected_payload, (
        "Bad payload " + response.json())


def log_in_wrong_password(email: str, password: str) -> None:
    """Function tp test wrong pwd"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert response.status_code == 401, "Unexpected: " + str(
        response.status_code)


def log_in(email: str, password: str) -> str:
    """Function to test right login"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """Function to test unlogged profile"""
    response = requests.get("http://127.0.0.1:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Function description generic"""
    response = session.get("http://127.0.0.1:5000/profile")
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Function to test the logout route"""
    response = session.delete("http://127.0.0.1:5000/sessions")
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Function description generic"""
    response = requests.post("http://127.0.0.1:5000/reset_password",
                             data={"email": email}
                             )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response.get('email') == email

    return json_response.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Function description generic"""
    response = requests.put(
        "http://127.0.0.1:5000/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
