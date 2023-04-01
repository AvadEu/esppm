import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import load_dotenv

from app.api.models.domain.users import User
from app.security.generate_hash import generate_hash
from app.security.jwt import JWTEngine

import os

load_dotenv()


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
    return User(
        username="test_username",
        first_name="test_firstname",
        last_name="test_lastname",
        password_hash=generate_hash("test_password")
    )


@pytest.fixture
def register_user() -> dict:
    return {
        "username": "test_username",
        "first_name": "test_firstname",
        "last_name": "test_lastname",
        "password": "password",
        "repeat_password": "password"
    }


@pytest.fixture
def record_response_model() -> dict:
    return {
        "record_id": 404,
        "service": "test_service1",
        "login": "decrypted_test_data",
        "password": "decrypted_test_data"
    }


@pytest.fixture
def token() -> str:
    SECRET = os.getenv("JWT_SECRET")
    engine = JWTEngine(
        secret=SECRET
            )
    return engine.encode({
        "username": "test_username",
        "first_name": "test_firstname",
        "last_name": "test_lastname"
    })


@pytest.fixture
def authorized_client(
    client: TestClient,
    token: str
        ) -> TestClient:
    client.headers = {
        "Authorization": f"Bearer {token}",
        **client.headers
    }
    return client
