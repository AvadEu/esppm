from app.api.db.DatabaseConnection import DatabaseConnection
from app.api.models.domain.records import Record
from app.api.models.domain.secrets import Secret
from app.api.models.domain.users import User
from app.utils.conf import read_conf

from typing import List

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


def get_secret_by_owner(owner: str) -> Secret | None:
    with db_connection.get_session() as session:
        res = session.query(Secret).filter(Secret.owner == owner)
    return res.first()


def get_all_records_by_owner(owner: str) -> List[Record]:
    with db_connection.get_session() as session:
        res = session.query(Record).filter(Record.owner == owner)
    return res.all()


def delete_obj_by_id(
        obj: Record | Secret,
        obj_id: int
        ) -> None:
    with db_connection.get_session() as session:
        res = session.query(obj).filter(obj.id == obj_id)
        if res.first():
            res.delete(synchronize_session=False)
            session.commit()
        else:
            raise ValueError(
                "There is no object type {} of id: {} in database!"
                .format(obj.__name__, obj_id)
                )


def delete_user_from_db(username: str) -> None:
    with db_connection.get_session() as session:
        user = session.query(User).filter(User.username == username)
        try:
            user_records = session.query(Record).filter(Record.owner == username)
            user_records.delete(synchronize_session=False)
            user_secret = session.query(Secret).filter(Secret.owner == username)
            user_secret.delete(synchronize_session=False)
        except Exception:
            pass
        finally:
            user.delete(synchronize_session=False)
            session.commit()
