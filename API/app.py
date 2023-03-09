import models
import uvicorn
import tomllib
from os import path
from fastapi import FastAPI

app = FastAPI()

# Function that reads application config and return it as a dictionary
def read_conf() -> dict:
    conf_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),'conf.toml')
    with open(conf_path, 'rb') as f:
        conf = tomllib.load(f)
        return conf


@app.get('/')
def hello_world():
    return {"Hello": 'World!'}


if __name__ == "__main__":
    api_conf, db_conf = list(read_conf().values()[:2])
    engine = models.init_all(db_conf)
    uvicorn.run('app:app', host=api_conf['host'], port=api_conf['port'], reload=api_conf['reload'])