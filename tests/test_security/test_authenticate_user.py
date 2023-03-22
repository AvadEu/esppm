from app.security.authenticate_user import authenticate_user
from tests.conftest import sample_user

from unittest import mock


@mock.patch(
        'app.security.authenticate_user.get_user_by_username',
        return_value=sample_user,
        autospec=True
)
def test_authenticate_user(mock_get_user_by_username, user):
    assert authenticate_user("test_username", "test_password") == user


@mock.patch(
        'app.security.authenticate_user.get_user_by_username',
        return_value=None,
        autospec=True
)
def test_authenticate_user_not_exists(mock_get_user_by_username):
    assert authenticate_user("not", "exists") is False
