import pytest
import requests

def test_register_user():
    url = "http://127.0.0.1:8000/register"
    data = {
        "email": "12",
        "password": "12",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "12"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Failed to register user: {response.text}" 