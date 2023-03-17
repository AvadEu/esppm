import uvicorn

from app.api import get_application
from app.utils.conf import read_conf

app = get_application()

if __name__ == '__main__':
    api_conf = read_conf(filename='conf.toml', conf_title='api_conf')
    config = uvicorn.Config("launch:app", **api_conf)
    server = uvicorn.Server(config=config)
    server.run()