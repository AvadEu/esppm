from fastapi import FastAPI

from app.api.pydantic_models import Register_form
from app.utils import read_conf, init_database

app = FastAPI()

db_conf = read_conf(filename='conf.toml', conf_title='db_conf')
engine = init_database(db_conf)

@app.get('/')
def hello_world():
    return {"Hello": 'World!'}


@app.post('/register')
def register(user: Register_form):
    pass


def get_application() -> FastAPI:
    return app
