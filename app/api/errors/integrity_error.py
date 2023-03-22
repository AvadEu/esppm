from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=406,
        content={'message': "This username is already taken"}
    )
