from ..security import generate_hash

from os import path
import random, string

def generate_jwt_secret():
    dotenv_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))),".env")
    random_sequence = "".join(random.choice(string.ascii_letters) for _ in range(16))
    random_hash = generate_hash(random_sequence)
    with open(dotenv_path, 'w+') as file:
        file.write(f'JWT_SECRET="{str(random_hash)}"')