from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pytest

from app.security.encryption.aes import encrypt, decrypt

import os

TO_ENCRYPT = "Secret message!"
KEY = os.urandom(32)
IV = os.urandom(16)


@pytest.fixture
def encrypted_payload() -> bytes:
    encryptor = Cipher(
        algorithm=algorithms.AES256(key=KEY),
        mode=modes.CFB(initialization_vector=IV)
    ).encryptor()
    payload = encryptor.update(TO_ENCRYPT.encode()) + encryptor.finalize()
    return payload


def test_encrypt(encrypted_payload) -> None:
    encrypted = encrypt(TO_ENCRYPT, KEY, IV)
    assert isinstance(encrypted, bytes)
    assert encrypted == encrypted_payload


def test_decrypt(encrypted_payload) -> None:
    decrypted = decrypt(
        ciphertext=encrypted_payload,
        key=KEY,
        initialization_vector=IV
        )
    assert isinstance(decrypted, str) 
    assert decrypted == TO_ENCRYPT
