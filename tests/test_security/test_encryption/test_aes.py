from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pytest

from app.security.encryption.aes import (
    __encrypt,
    __decrypt,
    encrypt_record,
    decrypt_record
)
from app.api.models.domain.records import Record
from app.api.models.schemas.records import RecordPydantic

import os
from unittest import mock

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
    encrypted = __encrypt(TO_ENCRYPT, KEY, IV)
    assert isinstance(encrypted, bytes)
    assert encrypted == encrypted_payload


def test_decrypt(encrypted_payload) -> None:
    decrypted = __decrypt(
        ciphertext=encrypted_payload,
        key=KEY,
        initialization_vector=IV
        )
    assert isinstance(decrypted, str)
    assert decrypted == TO_ENCRYPT


def test_encrypt_record(record_response_model) -> None:
    sample_record = RecordPydantic(
        service=record_response_model["service"],
        login=record_response_model["login"],
        password=record_response_model["password"]
    )
    encrypted_record = encrypt_record(
        username="test_owner",
        record=sample_record,
        key=KEY,
        initialization_vector=IV
    )
    decrypted_sample = decrypt_record(encrypted_record, KEY, IV)
    decrypted_sample["record_id"] = 404
    assert isinstance(encrypted_record, Record)
    assert decrypted_sample == record_response_model


@mock.patch(
    target="app.security.encryption.aes.__decrypt",
    return_value="decrypted_test_data",
    autospec=True
)
def test_decrypt_record(
    mock_decrypt_record,
    record_response_model
        ) -> None:
    sample_record = Record(
        service="test_service1",
        login=b"decrypted_test_data",
        password=b"decrypted_test_data",
        owner="test_owner",
        iv=b"iv"

    )
    sample_record.id = 404
    decrypted_record = decrypt_record(
        record=sample_record,
        key=b"SECRET",
        initialization_vector=b"IV")
    assert decrypted_record == record_response_model
