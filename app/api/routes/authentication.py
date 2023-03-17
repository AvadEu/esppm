from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv

from app.api.models.pydantic_models import UserPydantic
from app.api.db.services import get_user_by_username
from app.security.jwt import JWTEngine
from app.security import authenticate_user

import os

router = APIRouter()

load_dotenv()
jwt_engine = JWTEngine(
    secret=os.getenv('JWT_SECRET'), 
    algorithm=os.getenv("JWT_ALGORITHM")
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt_engine.decode(token)
        username = payload.get('username')
        user = get_user_by_username(username=username)
    except:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid Credentials'
        )
    pydantic_user = UserPydantic(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
        )
    return pydantic_user


@router.post('/token')
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials!"
        )
    token_payload = user.get_token_payload()
    token = jwt_engine.encode(token_payload)
    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.get('/private')
def private(user: UserPydantic = Depends(get_current_user)):
    return {'Access': "Granted"}