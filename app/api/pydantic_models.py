from pydantic import BaseModel

# Class to handle api "/register" post request body
class Register_form(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str