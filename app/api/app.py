from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from app.utils.conf import read_conf
import models


app = FastAPI()

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


if __name__ == "__main__":
    api_conf, db_conf = list(read_conf('conf.toml').values())[:2]
    engine = models.init_all(db_conf)
    uvicorn.run('app:app', host=api_conf['host'], port=api_conf['port'], reload=api_conf['reload'])