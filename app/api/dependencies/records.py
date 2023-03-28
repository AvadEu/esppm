from app.api.models.domain.records import Record
from app.api.models.schemas.records import RecordPydantic, RecordUpdatePydantic
from app.security.encryption.aes import encrypt_record, decrypt_record
from app.api.db.services import update_record_in_db


def update_record_data(
    username: str,
    key: bytes,
    old_record: Record,
    updated_record_body: RecordUpdatePydantic
        ) -> None:
    old_decrypted_record = decrypt_record(
        record=old_record,
        key=key,
        initialization_vector=old_record.iv
    )
    record_body_dict = {
        k: v for k, v in updated_record_body.dict().items() if v is not None
        }
    new_record_body = RecordPydantic(
        service=record_body_dict.get("service", old_decrypted_record["service"]),
        login=record_body_dict.get("login", old_decrypted_record["login"]),
        password=record_body_dict.get("password", old_decrypted_record["password"])
    )
    new_record_encrypted = encrypt_record(
        owner_username=username,
        record=new_record_body,
        key=key,
        initialization_vector=old_record.iv
    )
    update_record_in_db(
        old_decrypted=old_decrypted_record,
        new_record=new_record_encrypted
    )
