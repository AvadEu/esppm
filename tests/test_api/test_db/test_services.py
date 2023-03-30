import pytest
from sqlalchemy.exc import IntegrityError

from app.api.db.DatabaseConnection import DatabaseConnection
from app.utils.unittest_db import clean_test_database
from app.api.models.domain.users import User
from app.api.models.domain.records import Record
from app.api.models.domain.secrets import Secret
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


@pytest.fixture()
def test_user_payload(user: User) -> dict:
    payload = user.get_token_payload()
    payload["password_hash"] = user.password_hash
    return payload


@pytest.fixture
def test_record_body(
    record_response_model: dict,
    user: User
        ) -> Record:
    sample_record = Record(
        service=record_response_model.get('service'),
        login=record_response_model.get('login').encode(),
        password=record_response_model.get('password').encode(),
        iv=b'SECRET_VECTOR',
        owner=user.username
    )
    sample_record.id = 20
    sample_record.created_at = datetime.now()
    return sample_record


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_add_to_db(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_user_payload: dict,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    user.created_at = datetime.now()
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
    assert test_user_payload.get("username") == new_user_dict.get("username")
    assert test_user_payload.get("first_name") == new_user_dict.get("first_name")
    assert test_user_payload.get("last_name") == new_user_dict.get("last_name")
    assert test_user_payload.get("password_hash") == new_user_dict.get("password_hash")


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_get_user_by_username(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_user_payload: dict,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    username = test_user_payload.get("username")
    try:
        user.created_at = datetime.now()
        add_to_db(user)
    except IntegrityError:
        assert False
    user_from_db = get_user_by_username(username)
    print(user_from_db, username)
    assert test_user_payload.get("username") == user_from_db.username
    assert test_user_payload.get("first_name") == user_from_db.first_name
    assert test_user_payload.get("last_name") == user_from_db.last_name
    assert test_user_payload.get("password_hash") == user_from_db.password_hash


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_get_secret_by_owner(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    sample_content = b"SECRET"
    sample_secret = Secret(
        content=sample_content,
        owner=user.username
    )
    sample_secret.created_at = datetime.now()
    try:
        add_to_db(sample_secret)
    except IntegrityError:
        assert False
    res = get_secret_by_owner(user.username)
    assert res.content == sample_content
    assert res.owner == user.username
    assert isinstance(res, Secret)


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_get_record_by_id(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_record_body: Record,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    test_dict = test_record_body.to_dict()
    try:
        add_to_db(test_record_body)
    except IntegrityError:
        assert False
    res = get_record_by_id(test_dict.get('id'))
    assert res.password == test_dict.get("password")
    assert res.service == test_dict.get("service")
    assert res.login == test_dict.get("login")
    assert res.id == test_dict.get("id")
    assert res.iv == test_dict.get("iv")


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_get_all_records_by_owner(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_record_body: Record,
    user: User
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    test_dict = test_record_body.to_dict()
    try:
        add_to_db(test_record_body)
    except IntegrityError:
        assert False
    res = get_all_records_by_owner(owner=user.username)
    assert len(res) > 0
    res = res[0]
    assert res.password == test_dict.get("password")
    assert res.service == test_dict.get("service")
    assert res.login == test_dict.get("login")
    assert res.id == test_dict.get("id")
    assert res.iv == test_dict.get("iv")


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_delete_obj_by_id(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_record_body: Record,
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    id_to_remove = test_record_body.to_dict().get('id')
    try:
        add_to_db(test_record_body)
    except IntegrityError:
        assert False
    delete_obj_by_id(obj=Record, obj_id=id_to_remove)
    with pytest.raises(ValueError):
        get_record_by_id(record_id=id_to_remove)


@mock.patch(target="app.api.db.services.db_connection.get_engine")
def test_update_record_in_db(
    mock_db_get_engine: mock.MagicMock,
    test_database_connection: DatabaseConnection,
    test_record_body: Record,
        ) -> None:
    mock_db_get_engine.return_value = test_database_connection.get_engine()
    updated_record = Record(
        service="different_service",
        login=test_record_body.login,
        password=test_record_body.password,
        owner=test_record_body.owner,
        iv=test_record_body.iv
    )
    updated_record.id = test_record_body.id
    updated_record.created_at = test_record_body.created_at
    old_decrypted = test_record_body.to_dict()
    old_decrypted["record_id"] = old_decrypted.get('id')
    try:
        add_to_db(test_record_body)
    except IntegrityError:
        assert False
    update_record_in_db(old_decrypted=old_decrypted, new_record=updated_record)
    try:
        res = get_record_by_id(record_id=old_decrypted.get('id'))
    except ValueError:
        assert False
    assert res.service == "different_service"
