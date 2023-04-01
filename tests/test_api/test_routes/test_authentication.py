import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from starlette import status

from app.api.routes.authentication import get_current_user
from app.api.models.schemas.users import UserPydantic
from app.api.models.domain.users import User

from unittest import mock


@mock.patch(
        target='app.api.routes.authentication.get_user_by_username',
        autospec=True
)
def test_get_current_user(
    mocked_get_user_by_username: mock.MagicMock,
    token: str,
    user: User
        ) -> None:
    mocked_get_user_by_username.return_value = user
    sample_pydantic = UserPydantic(
        username='test_username',
        first_name='test_firstname',
        last_name='test_lastname'
    )
    res = get_current_user(token)
    assert res == sample_pydantic


@mock.patch(
        target='app.api.routes.authentication.get_user_by_username',
        autospec=True
)
def test_get_current_user_bad_token(
    mocked_get_user_by_username: mock.MagicMock,
    user: User
        ) -> None:
    mocked_get_user_by_username.return_value = user
    with pytest.raises(HTTPException):
        get_current_user("BAD TOKEN")


@mock.patch(
        target='app.api.routes.authentication.authenticate_user',
        autospec=True
)
def test_login_for_token(
    mock_authenticate_user: mock.MagicMock,
    user: User,
    token: str,
    client: TestClient
        ) -> None:
    mock_authenticate_user.return_value = user
    form_data = {
        'username': 'test_username',
        'password': 'test_password'
    }
    proper_response = {
        'access_token': token,
        'token_type': 'bearer'
    }
    response = client.post(
        url="/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=form_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == proper_response


@mock.patch(
        target='app.api.routes.authentication.authenticate_user',
        autospec=True
)
def test_login_for_token_bad_credentials(
    mock_authenticate_user: mock.MagicMock,
    client: TestClient
        ) -> None:
    mock_authenticate_user.return_value = False
    form_data = {
        'username': 'bad_data',
        'password': 'bad_data'
    }
    response = client.post(
        url="/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=form_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid Credentials!"}
