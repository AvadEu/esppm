import pytest

from app.api.models.domain.users import User
from app.security.generate_hash import generate_hash


sample_user =  User(
        username="test_username",
        first_name="test_firstname",
        last_name="test_lastname",
        password_hash=generate_hash("test_password")
    )

@pytest.fixture
def user() -> User:
    return sample_user