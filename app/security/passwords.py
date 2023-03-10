from cryptography.hazmat.primitives import hashes

# Class for user password hashing
class PasswordObject():
    def __init__(self, password: str):
        self.password = password
    
    def hash_password(self) -> bytes:
        """
        Method that takes object provided password and convert it to the hash
        using SHA265 algorithm and return bytes
        """
        digest = hashes.Hash(hashes.SHA256())
        digest.update((self.password).encode())
        return digest.finalize()
    
    def verify(self, hash: bytes) -> bool:
        """
        Function that takes one argument which is password hash and verifies if
        it match with the password from the object constructor.
        """
        if self.hash_password(self.password) == hash:
            return True
        else:
            return False