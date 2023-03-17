from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from app.api.models.orm import Base

class DatabaseConnection():
    """
    Constructor takes one argument: dictionary with keys [username, password, host, db_name] 
    to connect to postgres database using psycopg2 connector. 
    """
    def __init__(self, conf: dict) -> None:
        self.conf = conf
        self.connection_string = "postgresql+psycopg2://{username}:{password}@{host}/{db_name}".format(
            username=self.conf['username'],
            password=self.conf['password'],
            host=self.conf['host'],
            db_name=self.conf['db_name']
        )

    def get_engine(self, echo: bool = False) -> Engine:
        self.engine = create_engine(self.connection_string, echo=echo)
        return self.engine
    
    def get_session(self) -> Session:
        new_session = Session(self.get_engine())
        return new_session
    
    def init_all(self) -> None:
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
