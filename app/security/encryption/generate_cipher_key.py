from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def generate_cipher_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=16,
        p=2
    )
    key = kdf.derive(password.encode())
    return key
