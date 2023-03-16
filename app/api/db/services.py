from app.api.models.orm import User, Secret, Record
from app.utils.conf import read_conf
from . import DatabaseConnection

db_config = read_conf(conf_title="db_conf", filename='dev_conf.toml')
db_connection = DatabaseConnection(db_config)
db_connection.get_engine()
db_connection.init_all()


def add_to_db(obj: User | Secret | Record) -> None:
    with db_connection.get_session() as session:
        session.add(obj)
        session.commit()


def get_user_by_username(username: str) -> User | None:
    with db_connection.get_session() as session:
        res = session.query(User).filter(User.username == username).first()
    return res