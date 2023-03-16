from app.api.models import User
from .generate_hash import generate_hash

from sqlalchemy.engine.base import Engine

def authenticate_user(engine: Engine, username: str, password: str) -> bool | User:
    user = User.get_user_by_username(engine = engine, username=username)
    if user and user.password_hash == generate_hash(password):
        return user
    else:
        return False
