from fastapi import status
from test.utils import *



def test_create_user():
    request_data = {
        "username": "final_test_user",
        "email": "final@example.com",
        "password": "testpassword123",
        "first_name": "Mohamed",
        "last_name": "Dawod",
        "phone_number": "01234567890"
    }
    response = client.post("/users/register", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_login_for_access_token():

    login_data = {
        "username": "final_test_user",
        "password": "testpassword123"
    }

    response = client.post("/users/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_update_user_information():
    update_data = {
        "username": "final_test_user",
        "email": "updated_final@example.com",
        "password": "newpassword123",
        "first_name": "Mohamed",
        "last_name": "Updated",
        "phone_number": "01234567899"
    }
    response = client.put("/users/update", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["last_name"] == "Updated"
    assert response.json()["phone_number"] == "01234567899"