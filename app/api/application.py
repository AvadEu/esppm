from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI

from app.api.errors import integrity_error_handler
from app.api.routes.router import api_router


def get_application() -> FastAPI:

    application = FastAPI()

    application.include_router(api_router)

    application.add_exception_handler(IntegrityError, integrity_error_handler)

    return application


app = get_application()
