from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from app.api.errors import integrity_error_handler
from app.api.pydantic_models import Register_form
from app.security import generate_hash, authenticate_user
from app.utils import read_conf, init_database
from app.api import models

app = FastAPI()
app.add_exception_handler(IntegrityError, integrity_error_handler)

db_conf = read_conf(filename='dev_conf.toml', conf_title='db_conf')
engine = init_database(db_conf)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_user = authenticate_user(engine, form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_payload = auth_user.get_token_payload()
    token = jwt.encode(token_payload, "secret")
    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@app.get('/')
def hello_world():
    return {'Hello': 'world!'}


@app.post('/register')
def register_user(user: Register_form):
    if not user.password == user.repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    password_hash = generate_hash(user.password)
    new_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name, 
        password_hash=password_hash 
        )
    new_user.add_to_db(engine=engine)
    return {"detail": "Added successfully"}


def get_application() -> FastAPI:
    return app
