
from fastapi.testclient import TestClient
from starlette import status

from unittest import mock
from typing import Callable


def get_new_record_dict() -> dict:
    return {
        "service": "test_service",
        "login": "test_login",
        "password": "test_password",
        "vault_password": "vault_password"
    }


@mock.patch(
        target="app.api.routes.records.add_to_db",
        return_value="None",
        autospec=True
)
def test_add_record_proper(
    mock_add_to_db: Callable,
    authorized_client: TestClient
        ) -> None:
    response = authorized_client.post(
        url="/records/add",
        json=get_new_record_dict()
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': 'Record added successfully'}


def test_add_record_no_auth(
    client: TestClient
        ) -> None:
    response = client.post(
        url="/records/add",
        json=get_new_record_dict()
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_record_bad_data(
    authorized_client: TestClient
        ) -> None:
    response = authorized_client.post(
        url="/records/add",
        json={"service": "test_service"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mock.patch(
    target="app.api.routes.records.decrypt_record",
    autospec=True
)
def test_get_records_proper(
    mock_decrypt_record: Callable,
    record_response_model: Callable,
    authorized_client: TestClient
        ) -> None:
    mock_decrypt_record.return_value = record_response_model
    response = authorized_client.post(
        url="/records",
        json={"vault_password": "test_vault_password"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] == record_response_model


def test_get_records_no_auth(
    client: TestClient
        ) -> None:
    response = client.post(
        url="records",
        json={"vault_password": "test_vault_password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@mock.patch(
        target="app.api.routes.records.delete_obj_by_id",
        return_value=None,
        autospec=True
)
def test_delete_record_proper(
    mock_delete_obj_by_id: mock.MagicMock,
    authorized_client: TestClient
        ) -> None:
    response = authorized_client.delete(
        url="/records/delete",
        params={"record_id": 5}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Record deleted successfully!"}


@mock.patch(
        target="app.api.routes.records.delete_obj_by_id",
        return_value=None,
        autospec=True
)
def test_delete_record_not_exists(
    mock_delete_obj_by_id: mock.MagicMock,
    authorized_client: TestClient
        ) -> None:
    mock_delete_obj_by_id.side_effect = ValueError()
    response = authorized_client.delete(
        url="/records/delete",
        params={"record_id": 5}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
