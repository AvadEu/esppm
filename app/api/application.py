from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI

from app.api.errors import integrity_error_handler
from app.api.routes import users, authentication


def get_application() -> FastAPI:
    
    application = FastAPI()
    
    application.include_router(users.router)
    application.include_router(authentication.router)

    application.add_exception_handler(IntegrityError, integrity_error_handler)
    
    return application
