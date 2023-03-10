from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from app.utils.conf import read_conf
import app.api.models as models


app = FastAPI()
db_conf = read_conf(filename='conf.toml', conf_title='db_conf')

# Class to handle api "/register" post request body
class Register_form(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


@app.get('/')
def hello_world():
    return {"Hello": 'World!'}


@app.post('/register')
def register(user: Register_form):
    pass


def get_application() -> FastAPI:
    engine = models.init_all(db_conf)
    return app
