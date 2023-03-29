import pytest

from app.api.db.DatabaseConnection import DatabaseConnection
from app.utils.unittest_db import clean_test_database
from app.api.models.domain.users import User
from app.api.db.services import (
    get_all_records_by_owner,
    get_user_by_username,
    get_secret_by_owner,
    update_record_in_db,
    delete_user_from_db,
    get_record_by_id,
    delete_obj_by_id,
    add_to_db
)

import sqlite3
from unittest import mock
from datetime import datetime


@pytest.fixture
def test_database_connection() -> DatabaseConnection:
    clean_test_database()
    test_db_con = DatabaseConnection("sqlite:///test.db")
    test_db_con.get_engine()
    test_db_con.init_all()
    return DatabaseConnection("sqlite:///test.db")


@pytest.fixture
def manual_database_connection() -> sqlite3.Cursor:
    con = sqlite3.connect("test.db")
    cur = sqlite3.Cursor(con)
    con.close()
    return cur


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_add_to_db(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    user.created_at = datetime.now()
    payload = user.get_token_payload()
    payload["password_hash"] = user.password_hash
    add_to_db(user)
    con = sqlite3.connect("test.db")
    cur = sqlite3.Cursor(con)
    res = cur.execute("SELECT * FROM Users;")
    user_data = res.fetchone()  # (id, username, f_name, l_name, pass_hash, created_at)
    con.close()
    new_user_dict = {
        "username": user_data[1],
        "first_name": user_data[2],
        "last_name": user_data[3],
        "password_hash": user_data[4]
    }
    assert payload.get("username") == new_user_dict.get("username")
    assert payload.get("first_name") == new_user_dict.get("first_name")
    assert payload.get("last_name") == new_user_dict.get("last_name")
    assert payload.get("password_hash") == new_user_dict.get("password_hash")
