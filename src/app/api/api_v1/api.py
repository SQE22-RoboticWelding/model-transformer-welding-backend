from fastapi import APIRouter
from app.api.api_v1.endpoints import test, robot_type

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["test", "database"])
