from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from app.api.models.schemas.users import UserPydantic
from app.api.models.schemas.records import (
    RecordUpdatePydantic,
    RecordPydantic,
    GetRecords
)
from app.api.models.domain.records import Record
from app.api.routes.authentication import get_current_user
from app.security.encryption.aes import encrypt_record, decrypt_record
from app.security.encryption.generate_cipher_key import generate_cipher_key
from app.api.dependencies.records import update_record_data
from app.api.db.services import (
    add_to_db,
    get_secret_by_owner,
    get_record_by_id,
    get_all_records_by_owner,
    delete_obj_by_id
    )

import os

router = APIRouter()


@router.post('/records/add')
def add_record(
    record: RecordPydantic,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    secret = get_secret_by_owner(owner=user.username)
    initial_vector = os.urandom(16)
    enc_key = generate_cipher_key(
        password=record.vault_password,
        salt=secret.content
    )
    new_record = encrypt_record(
        owner_username=user.username,
        record=record,
        key=enc_key,
        initialization_vector=initial_vector
    )
    add_to_db(new_record)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'detail': 'Record added successfully'}
    )


@router.post('/records')
def get_records(
    body: GetRecords,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    all_records = get_all_records_by_owner(owner=user.username)
    secret = get_secret_by_owner(owner=user.username)
    output = []
    dec_key = generate_cipher_key(
        password=body.vault_password,
        salt=secret.content
    )
    for record in all_records:
        new_record = decrypt_record(
            record=record,
            key=dec_key,
            initialization_vector=record.iv
        )
        output.append(new_record)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output
    )


@router.put("/records/update")
def update_record(
    record_id: int,
    record_body: RecordUpdatePydantic,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    secret = get_secret_by_owner(owner=user.username)
    try:
        dec_key = generate_cipher_key(
            password=record_body.vault_password,
            salt=secret.content
        )
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vault password have not been provided!"
        )
    try:
        old_record = get_record_by_id(record_id=record_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no record of id {} in database"
            .format(record_id)
        )
    update_record_data(
        username=user.username,
        key=dec_key,
        old_record=old_record,
        updated_record_body=record_body
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Record updated successfully!"}
    )


@router.delete('/records/delete')
def delete_record(
    record_id: int,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    try:
        delete_obj_by_id(
            obj=Record,
            obj_id=record_id
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There's no record of id {}".format(record_id)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail': 'Record deleted successfully!'}
    )
