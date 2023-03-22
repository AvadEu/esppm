import pytest
from starlette import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from unittest import mock


@pytest.fixture
def register_user() -> dict:
    return {
        "username": "test_username",
        "first_name": "test_firstname",
        "last_name": "test_lastname",
        "password": "password",
        "repeat_password": "password"
    }


@mock.patch(
        target="app.api.routes.users.add_to_db",
        return_value=None,
        autospec=True
    )
def test_users_register_correct(
    mock_add_to_db,
    register_user: dict,
    client: TestClient
        ) -> None:
    response = client.post(
        url="/register",
        json=register_user
        )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "User added successfully!"}


@mock.patch(
        target="app.api.routes.users.add_to_db",
        return_value=None,
        autospec=True
    )
def test_users_register_not_unique_username(
    mock_add_to_db,
    register_user: dict,
    client: TestClient
        ) -> None:
    mock_add_to_db.side_effect = IntegrityError(None, None, BaseException)
    response = client.post(
        url="/register",
        json=register_user
    )
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json() == {"detail": "Username already taken!"}


@mock.patch(
        target="app.api.routes.users.add_to_db",
        return_value=None,
        autospec=True
    )
def test_users_register_passwords_not_match(
    mock_add_to_db,
    register_user: dict,
    client: TestClient
        ) -> None:
    register_user["repeat_password"] = "random_password"
    response = client.post(
        url="/register",
        json=register_user
            )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Passwords do not match!"}


@mock.patch(
        target="app.api.routes.users.add_to_db",
        return_value=None,
        autospec=True
    )
def test_user_register_bad_data(
    mock_add_to_db,
    register_user: dict,
    client: TestClient
        ) -> None:
    register_user.pop("first_name")
    response = client.post(
        url="/register",
        json=register_user
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
