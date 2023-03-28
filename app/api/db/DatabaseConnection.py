from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from app.api.models.domain.base import Base


class DatabaseConnection():
    def __init__(self, db_path: str) -> None:
        self.connection_string = db_path

    def get_engine(self, echo: bool = False) -> Engine:
        self.engine = create_engine(self.connection_string, echo=echo)
        return self.engine

    def get_session(self) -> Session:
        new_session = Session(self.get_engine())
        return new_session

    def init_all(self) -> None:
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
