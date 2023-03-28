from app.api.db.DatabaseConnection import DatabaseConnection
from app.api.models.domain.records import Record
from app.api.models.domain.secrets import Secret
from app.api.models.domain.users import User
from dotenv import load_dotenv

import os
from typing import List

load_dotenv()
db_connection = DatabaseConnection(os.getenv("DB_PATH"))
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


def get_record_by_id(record_id: int) -> Record:
    with db_connection.get_session() as session:
        res = session.query(Record).filter(Record.id == record_id).first()
    if res is None:
        raise ValueError("There's no record of id: {} in database!".format(record_id))
    else:
        return res


def update_record_in_db(
    old_decrypted: dict,
    new_record: Record
        ) -> None:
    with db_connection.get_session() as session:
        session.query(Record)\
            .filter(Record.id == old_decrypted["record_id"])\
            .update({
                "service": new_record.service,
                "login": new_record.login,
                "password": new_record.password
            })
        session.commit()
    return None


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
