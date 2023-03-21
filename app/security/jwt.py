import jwt

import random, string
from datetime import datetime, timedelta

class JWTEngine():
    def __init__(
            self, 
            secret: str | None = None,
            algorithm: str = "HS512", 
            key_length: int = 64
        ) -> None:
        self.algorithm = algorithm
        if secret:
            self.secret = secret
        else:
            self.key_length = key_length
            self.secret = self.__generate_secret()


    def __generate_secret(self) -> str:
        secret_key = "".join(
            random.choice(string.hexdigits) for _ in range(self.key_length)
        )
        return secret_key


    def encode(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=10)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt


    def decode(self, to_decode: str) -> dict:
        try:
            payload = jwt.decode(to_decode, self.secret, algorithms=[self.algorithm])
        except jwt.PyJWTError:
            raise ValueError("Unable to decode JWT token")
        return payload