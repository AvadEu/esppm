from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from app.api.models.domain.records import Record
from app.api.models.schemas.records import RecordPydantic


def __encrypt(to_encrypt: str, key: bytes, initialization_vector: bytes) -> bytes:
    to_encrypt = to_encrypt.encode()
    encryptor = Cipher(
        algorithm=algorithms.AES256(key=key),
        mode=modes.CFB(initialization_vector)
    ).encryptor()
    ciphertext = encryptor.update(to_encrypt) + encryptor.finalize()
    return ciphertext


def __decrypt(ciphertext: bytes, key: bytes, initialization_vector: bytes) -> str:
    decryptor = Cipher(
        algorithm=algorithms.AES256(key=key),
        mode=modes.CFB(initialization_vector)
    ).decryptor()
    plain = decryptor.update(ciphertext) + decryptor.finalize()
    return plain.decode()


def encrypt_record(
    username: str,
    record: RecordPydantic,
    key: bytes,
    initialization_vector: bytes
            ) -> Record:
    encrypted_record = Record(
        service=record.service,
        login=__encrypt(record.login, key, initialization_vector),
        password=__encrypt(record.password, key, initialization_vector),
        owner=username,
        iv=initialization_vector
    )
    return encrypted_record


def decrypt_record(
    record: Record,
    key: bytes,
    initialization_vector: bytes
        ) -> dict:
    decrypted_record = {
        "record_id": record.id,
        "service": record.service,
        "login": __decrypt(record.login, key, initialization_vector),
        "password": __decrypt(record.password, key, initialization_vector)
    }
    return decrypted_record
