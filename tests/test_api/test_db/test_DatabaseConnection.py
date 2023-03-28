import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from app.api.db.DatabaseConnection import DatabaseConnection
from app.utils.unittest_db import clean_test_database

import sqlite3


@pytest.fixture
def database_connection() -> DatabaseConnection:
    clean_test_database()
    return DatabaseConnection("sqlite:///test.db")


@pytest.mark.order(1)
def test_get_engine(
    database_connection: DatabaseConnection
        ) -> None:
    eng = database_connection.get_engine()
    assert isinstance(eng, Engine)


def test_get_session(
    database_connection: DatabaseConnection
        ) -> None:
    session = database_connection.get_session()
    assert isinstance(session, Session)


@pytest.mark.order(2)
def test_init_all(
    database_connection: DatabaseConnection
        ) -> None:
    # It have to be ordered alphabetically
    table_names = ("Records", "Secrets", "Users")
    database_connection.get_engine()
    database_connection.init_all()
    con = sqlite3.connect("test.db")
    cur = sqlite3.Cursor(con)
    res = cur.execute(
        "SELECT name FROM sqlite_schema WHERE "
        "type = \'table\' AND name "
        "NOT LIKE \'sqlite_%\' ORDER BY 1;")
    tables = res.fetchall()
    con.close()
    tables = [x[0] for x in tables]
    for a, b in zip(tables, table_names):
        assert a == b
