import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {"Hello": 'World!'}


if __name__ == "__main__":
    uvicorn.run('app:app', host='127.0.0.1', port=4040)