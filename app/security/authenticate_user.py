from app.api.db.services import get_user_by_username
from app.api.models.orm import User
from .generate_hash import generate_hash

def authenticate_user(username: str, password: str) -> bool | User:
    user = get_user_by_username(username=username)
    if user and user.password_hash == generate_hash(password):
        return user
    else:
        return False
