from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt(to_encrypt: str, key: bytes, initialization_vector: bytes) -> bytes:
    to_encrypt = to_encrypt.encode()
    encryptor = Cipher(
        algorithm=algorithms.AES256(key=key),
        mode=modes.CFB(initialization_vector)
    ).encryptor()
    ciphertext = encryptor.update(to_encrypt) + encryptor.finalize()
    return ciphertext


def decrypt(ciphertext: bytes, key: bytes, initialization_vector: bytes) -> str:
    decryptor = Cipher(
        algorithm=algorithms.AES256(key=key),
        mode=modes.CFB(initialization_vector)
    ).decryptor()
    plain = decryptor.update(ciphertext) + decryptor.finalize()
    return plain.decode()
