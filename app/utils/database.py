from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine

from app.api.models import Base

# Creates database schema and returns engine 
def init_database(conf: dict) -> Engine:
    """
    Function takes one argument: dictionary with keys [username, password, host, db_name] to connect to
    postgres database using psycopg2 connector. It build entire database schema declared in
    models.py file and returns sqlalchemy.engine.base.Engine object of that database.
    """
    engine = create_engine(f"postgresql+psycopg2://{conf['username']}:{conf['password']}@{conf['host']}/{conf['db_name']}", echo=True)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    return engine