from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.models.pydantic_models import Register_form
from app.api.db.services import add_to_db
from app.api.models import orm as models
from app.security import generate_hash

router = APIRouter()

@router.post('/register')
def register_user(user: Register_form):
    if not user.password == user.repeat_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, 
            detail="Passwords do not match!"
            )
    
    password_hash = generate_hash(user.password)
    new_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name, 
        password_hash=password_hash 
        )
    add_to_db(new_user)
    
    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={"detail": "User added successfully"}
    )