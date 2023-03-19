from pydantic import BaseModel

# Class to handle api "/register" post request body
class RegisterUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str


class UserPydantic(BaseModel):
    username: str
    first_name: str
    last_name: str