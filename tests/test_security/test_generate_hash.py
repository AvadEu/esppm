import pytest

from app.security.generate_hash import generate_hash

@pytest.fixture
def hashed():
    return generate_hash("Test sentence")

def test_hash_is_bytes(hashed):
    assert isinstance(hashed, bytes)


def test_hashes_match(hashed):
    h2 = generate_hash("Test sentence")
    assert h2 == hashed