import jwt
import pytest

from app.security.jwt import JWTEngine

TEST_SECRET = 'secret'
TEST_ALGORITHM = "HS512"

@pytest.fixture
def content() -> dict:
    return {"content": "payload"}


def test_create_jwt_token_secret_provided(content) -> None:
    engine = JWTEngine(
        secret=TEST_SECRET,
        algorithm=TEST_ALGORITHM
    )
    token = engine.encode(content)
    parsed_payload = jwt.decode(token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
    assert parsed_payload["content"] == content["content"]


def test_create_jwt_token_without_secret(content) -> None:
    engine = JWTEngine(
        algorithm=TEST_ALGORITHM
    )
    token = engine.encode(content)
    parsed_payload = jwt.decode(token, engine.secret, algorithms=[TEST_ALGORITHM])
    assert parsed_payload["content"] == content["content"]


def test_decode_jwt_token(content) -> None:
    token = jwt.encode(content, TEST_SECRET, algorithm="HS512")
    engine = JWTEngine(
        secret=TEST_SECRET,
    )
    payload = engine.decode(token)
    assert payload["content"] == content["content"]


def test_error_when_wrong_token() -> None:
    engine = JWTEngine()
    with pytest.raises(ValueError):
        engine.decode("Bad Token")
