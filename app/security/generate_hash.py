from cryptography.hazmat.primitives import hashes


def generate_hash(token: str) -> bytes:
    """Function takes string as an argument and return hash
    of this string using SHA256 hashing algorithm"""
    token_bytes = token.encode()
    digest = hashes.Hash(hashes.SHA256())
    digest.update(token_bytes)
    return digest.finalize()
