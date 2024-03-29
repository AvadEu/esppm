from pydantic import BaseModel


class RecordPydantic(BaseModel):
    service: str
    login: str
    password: str
    vault_password: str | None = None


class GetRecords(BaseModel):
    vault_password: str


class RecordUpdatePydantic(RecordPydantic):
    service: str | None = None
    login: str | None = None
    password: str | None = None
