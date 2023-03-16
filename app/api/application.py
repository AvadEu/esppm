from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI

from app.api.errors import integrity_error_handler
from app.api.routes import users

# @app.post('/token')
# def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     auth_user = authenticate_user(engine, form_data.username, form_data.password)
#     if not auth_user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token_payload = auth_user.get_token_payload()
#     token = jwt.encode(token_payload, "secret")
#     return {
#         'access_token': token,
#         'token_type': 'bearer'
#     }

def get_application() -> FastAPI:

    application = FastAPI()
    
    application.include_router(users.router)

    application.add_exception_handler(IntegrityError, integrity_error_handler)
    
    return application
