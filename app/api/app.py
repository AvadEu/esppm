from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api.pydantic_models import Register_form
from app.utils import read_conf, init_database
from app.security import PasswordObject
from app.api import models

app = FastAPI()

db_conf = read_conf(filename='dev_conf.toml', conf_title='db_conf')
engine = init_database(db_conf)

@app.get('/')
def hello_world():
    return {"Hello": 'World!'}


@app.post('/register')
def register(user: Register_form):
    if not user.password == user.repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    with Session(engine) as session:
        user_password = PasswordObject(user.password)
        password_hash = user_password.hash_password()
        new_user = models.User(username=user.username, first_name=user.first_name, last_name=user.last_name, password_hash=password_hash)
        session.add(new_user)
        session.commit()
    return {"detail": "Added successfully"}


def get_application() -> FastAPI:
    return app
