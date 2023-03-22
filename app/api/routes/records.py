from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from app.api.models.schemas.users import UserPydantic
from app.api.models.schemas.records import RecordPydantic, GetRecords
from app.api.models.domain.records import Record
from app.api.models.domain.secrets import Secret
from app.api.routes.authentication import get_current_user
from app.security.encryption.aes import encrypt, decrypt
from app.security.encryption.generate_cipher_key import generate_cipher_key
from app.api.db.services import (
    add_to_db,
    get_user_by_username,
    get_obj_by_owner,
    delete_obj_by_id
    )

import os

router = APIRouter()


@router.post('/records/add')
def add_record(
    record: RecordPydantic,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    owner = get_user_by_username(user.username)
    secret = get_obj_by_owner(obj=Secret, owner=owner.username)
    initial_vector = os.urandom(16)
    enc_key = generate_cipher_key(
        password=record.vault_password,
        salt=secret.content
    )
    new_record = Record(
        service=record.service,
        login=encrypt(record.login, enc_key, initial_vector),
        password=encrypt(record.password, enc_key, initial_vector),
        owner=owner.username,
        iv=initial_vector
    )
    add_to_db(new_record)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'detail': 'Record added successfully'}
    )


@router.get('/records')
def get_records(
    body: GetRecords,
    user: UserPydantic = Depends(get_current_user)
        ) -> JSONResponse:
    all_records = get_obj_by_owner(
        obj=Record,
        owner=user.username,
        all_objects=True
        )
    salt = get_obj_by_owner(obj=Secret, owner=user.username).content
    output = []
    dec_key = generate_cipher_key(body.vault_password, salt=salt)
    for record in all_records:
        new_record = {
            "service": record.service,
            "login": decrypt(record.login, dec_key, record.iv),
            "password": decrypt(record.password, dec_key, record.iv)
        }
        output.append(new_record)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output
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
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="There's no record of id {}".format(record_id)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail': 'Record deleted successfully'}
    )
