from app.security.encryption.generate_cipher_key import generate_cipher_key


def test_generate_cipher_key() -> None:
    key1 = generate_cipher_key("password1", b"salt1")
    key2 = generate_cipher_key("password2", b"salt1")
    assert key1 != key2


def test_generate_cipher_key_repeatability() -> None:
    salt = b"salt"
    password = "safePassword"
    key1 = generate_cipher_key(password, salt)
    key2 = generate_cipher_key(password, salt)
    assert key1 == key2
