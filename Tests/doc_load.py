import pytest
import requests
import random
import string


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def random_referrals(num_docs):
    return ','.join(str(random.randint(2, num_docs)) for _ in range(random.randint(1, 10)))


@pytest.fixture(scope="module")
def token():
    url = "http://127.0.0.1:80/login"
    credentials = {"username": "12", "password": "12"}
    response = requests.post(url, data=credentials)
    assert response.status_code == 200, f"Authentication failed: {response.text}"
    return response.json()["access_token"]


def test_load_documents(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "http://127.0.0.1:80/add_docs"
    for i in range(2):
        doc = {
            "name": random_string(10),
            "content": random_string(20),
            "referrals": "" #random_referrals(i)
            }
        response = requests.post(url, json=doc, headers=headers)
        assert response.status_code == 200, f"Failed to load document {i}: {response.text}"
