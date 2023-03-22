from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.models.schemas.users import RegisterUser
from app.api.db.services import add_to_db
from app.api.models.domain.users import User
from app.api.models.domain.secrets import Secret
from app.security import generate_hash

import os

router = APIRouter()


@router.post('/register')
def register_user(user: RegisterUser):
    if user.password != user.repeat_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Passwords do not match!"
            )

    password_hash = generate_hash(user.password)
    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password_hash=password_hash
        )
    users_secret = Secret(
        content=os.urandom(16),
        owner=user.username
    )
    add_to_db(new_user)
    add_to_db(users_secret)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={"detail": "User added successfully!"}
    )
