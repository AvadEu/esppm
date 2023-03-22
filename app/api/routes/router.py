from fastapi import APIRouter

from app.api.routes import users, authentication, records

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(authentication.router)
api_router.include_router(records.router)
