import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.models.domain.users import User
from app.security.generate_hash import generate_hash


sample_user = User(
        username="test_username",
        first_name="test_firstname",
        last_name="test_lastname",
        password_hash=generate_hash("test_password")
    )


@pytest.fixture
def app() -> FastAPI:
    # Local import for test purpose
    from app.api.application import get_application
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def user() -> User:
    return sample_user
