from app.api.db.DatabaseConnection import DatabaseConnection
from app.api.models.domain.records import Record
from app.api.models.domain.secrets import Secret
from app.api.models.domain.users import User
from app.utils.conf import read_conf

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


def get_obj_by_owner(
        obj: Record | Secret,
        owner: str,
        all_objects: bool = False
    ) -> list | None:
    with db_connection.get_session() as session:
        res = session.query(obj).filter(obj.owner == owner)
        if all_objects:
            return res.all()
        else:
            return res.first()
